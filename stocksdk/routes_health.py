"""深度健康检查路由：/health/deep。

与 /health 浅检查不同，这里对 iFinD/EM 各做一次**最小只读取数**，确认
会话真的活着、能取到数，并测时延。供本地/远程 Agent 与监控判断每个源的
ok/stale/down，而非只看进程是否存活。

设计要点：
- 复用 sessions.*_exec 的会话自愈（失效自动重登重试一次）。
- 全局锁串行化，不并发探活，避免与正常取数互踢单点登录会话。
- 任一源异常都不抛 5xx：整体仍返回 200，故障源标 status=down + 脱敏原因，
  让监控始终拿到结构化结果。
- 脱敏:只回错误类型/简短消息,绝不回 token、完整 URL、账号。
"""
import time
from typing import Any, Dict

from fastapi import APIRouter, Depends

from EmQuantAPI import c
from iFinDPy import THS_RealtimeQuotes

from stocksdk.security import rate_limit, require_key
from stocksdk.sessions import em_exec, ths_exec, lock

router = APIRouter(tags=["健康检查"])

# 探活用固定标的与最小指标（贵州茅台，流动性好、长期存续）。
_PROBE_CODE = "600519.SH"
_PROBE_CODE_EM = "600519.SH"
_THS_PROBE_INDICATORS = "latest"
_EM_PROBE_INDICATORS = "CLOSE"

# 脱敏：错误消息最多回这么多字符，避免泄漏长 URL/堆栈。
_MAX_REASON_LEN = 120


def _sanitize(exc: Any) -> str:
    """异常 → 简短脱敏原因（类型 + 截断消息），不泄凭据/URL。"""
    text = "{}: {}".format(type(exc).__name__, exc)
    if len(text) > _MAX_REASON_LEN:
        text = text[:_MAX_REASON_LEN] + "…"
    return text


def _probe_ths() -> Dict[str, Any]:
    """iFinD 实时快照探活。返回 {status, latency_ms[, reason]}。"""
    start = time.perf_counter()
    try:
        r = ths_exec(lambda: THS_RealtimeQuotes(_PROBE_CODE, _THS_PROBE_INDICATORS, ""))
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        code = r.get("errorcode") if isinstance(r, dict) else None
        if code in (0, None):
            return {"status": "ok", "latency_ms": latency_ms}
        return {
            "status": "down",
            "latency_ms": latency_ms,
            "reason": "errorcode={}".format(code),
        }
    except Exception as e:   # SDK 底层(C++)异常/重登失败：标 down，不外抛
        return {
            "status": "down",
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "reason": _sanitize(e),
        }


def _probe_em() -> Dict[str, Any]:
    """EM 截面数据探活。返回 {status, latency_ms[, reason]}。"""
    start = time.perf_counter()
    try:
        r = em_exec(lambda: c.css(_PROBE_CODE_EM, _EM_PROBE_INDICATORS, "Ispandas=1"))
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        # Ispandas=1 正常返回 DataFrame；出错时是带 ErrorCode 的对象。
        err = getattr(r, "ErrorCode", 0)
        if err in (0, None):
            return {"status": "ok", "latency_ms": latency_ms}
        return {
            "status": "down",
            "latency_ms": latency_ms,
            "reason": "ErrorCode={}".format(err),
        }
    except Exception as e:
        return {
            "status": "down",
            "latency_ms": round((time.perf_counter() - start) * 1000, 1),
            "reason": _sanitize(e),
        }


@router.get("/health/deep")
def health_deep(_=Depends(require_key), __=Depends(rate_limit)):
    """深度健康检查：实测 iFinD + EM 各取一笔最小数据，返回每源状态与时延。

    整体始终 200；故障源在自身 status 里体现，便于监控/Agent 解析。
    """
    with lock:
        ifind = _probe_ths()
        em = _probe_em()
    overall = "ok" if ifind["status"] == "ok" and em["status"] == "ok" else "degraded"
    return {
        "status": overall,
        "ifind": ifind,
        "em": em,
        "as_of": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
