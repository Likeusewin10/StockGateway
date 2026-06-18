"""股票数据 HTTP 服务：其他项目通过 ip:端口 + 参数取数，无需写 SDK 代码。

启动（在 .venv-api 下）：
    .venv-api\\Scripts\\python -m uvicorn app:app --host 0.0.0.0 --port 8000

说明：
- 两个 SDK 均单会话/单点登录，本服务用全局锁串行化所有请求，
  必须单 worker 运行（不要加 --workers）。
- 默认无鉴权，仅限内网使用。不要直接暴露到公网。
- 交互式文档：http://<ip>:8000/docs
"""
import os
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

# ---- 加载 .env ----
for _line in Path(__file__).with_name(".env").read_text(encoding="utf-8").splitlines():
    _line = _line.strip()
    if _line and not _line.startswith("#") and "=" in _line:
        _k, _, _v = _line.partition("=")
        os.environ.setdefault(_k.strip(), _v.strip())

from EmQuantAPI import c
from iFinDPy import (
    THS_iFinDLogin,
    THS_iFinDLogout,
    THS_HistoryQuotes,
    THS_BasicData,
    THS_RealtimeQuotes,
)

# 全局锁：SDK 单会话，所有取数串行化
_lock = threading.Lock()
_em_ready = False
_ths_ready = False


def _ensure_em():
    global _em_ready
    if not _em_ready:
        r = c.start("ForceLogin=1", "")
        if r.ErrorCode != 0:
            raise HTTPException(502, "EM 登录失败：{} {}".format(r.ErrorCode, r.ErrorMsg))
        _em_ready = True


def _ensure_ths():
    global _ths_ready
    if not _ths_ready:
        code = THS_iFinDLogin(os.environ["THS_USER"], os.environ["THS_PWD"])
        if code != 0:
            raise HTTPException(502, "iFinD 登录失败：{}".format(code))
        _ths_ready = True


def _em_result(result):
    """EM 返回统一成 JSON 友好结构。Ispandas=1 时直接是 DataFrame。"""
    import pandas as pd
    if isinstance(result, tuple) and len(result) == 2:
        result = result[1]
    if isinstance(result, pd.DataFrame):
        return result.reset_index().to_dict(orient="records")
    if hasattr(result, "ErrorCode") and result.ErrorCode != 0:
        raise HTTPException(502, "EM 取数失败：{} {}".format(result.ErrorCode, result.ErrorMsg))
    return getattr(result, "Data", result)


app = FastAPI(title="股票数据服务", description="EM + iFinD 统一取数接口")

# ---- API Key 鉴权 ----
# .env 里设了 API_KEY 则所有取数接口要求请求头 X-API-Key 匹配；留空则不鉴权。
_API_KEY = os.environ.get("API_KEY", "").strip()
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_key(key: str = Security(_api_key_header)):
    if not _API_KEY:          # 未配置 key：不鉴权（仅本机/内网场景）
        return
    if key != _API_KEY:
        raise HTTPException(401, "缺少或错误的 X-API-Key")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/em/csd")
def em_csd(codes: str, indicators: str, startdate: str, enddate: str, options: str = "", _=Depends(require_key)):
    """东财序列数据。例：/em/csd?codes=300059.SZ&indicators=CLOSE&startdate=2024-01-01&enddate=2024-01-05"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with _lock:
        _ensure_em()
        return _em_result(c.csd(codes, indicators, startdate, enddate, opts))


@app.get("/em/css")
def em_css(codes: str, indicators: str, options: str = "", _=Depends(require_key)):
    """东财截面数据。例：/em/css?codes=300059.SZ,000002.SZ&indicators=OPEN,CLOSE&options=TradeDate=20240105"""
    opts = (options + ",Ispandas=1").lstrip(",") if "Ispandas" not in options else options
    with _lock:
        _ensure_em()
        return _em_result(c.css(codes, indicators, opts))


@app.get("/ths/history")
def ths_history(codes: str, indicators: str, begin: str, end: str, params: str = "", _=Depends(require_key)):
    """同花顺历史行情。例：/ths/history?codes=300033.SZ&indicators=open;close&begin=2024-01-01&end=2024-01-05"""
    with _lock:
        _ensure_ths()
        r = THS_HistoryQuotes(codes, indicators, params, begin, end)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@app.get("/ths/basic")
def ths_basic(codes: str, indicators: str, params: str = "", _=Depends(require_key)):
    """同花顺基础/截面数据。"""
    with _lock:
        _ensure_ths()
        r = THS_BasicData(codes, indicators, params)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r


@app.get("/ths/realtime")
def ths_realtime(codes: str, indicators: str, params: str = "", _=Depends(require_key)):
    """同花顺实时行情。"""
    with _lock:
        _ensure_ths()
        r = THS_RealtimeQuotes(codes, indicators, params)
    if r.get("errorcode") not in (0, None):
        raise HTTPException(502, "iFinD 取数失败：{} {}".format(r.get("errorcode"), r.get("errmsg")))
    return r
