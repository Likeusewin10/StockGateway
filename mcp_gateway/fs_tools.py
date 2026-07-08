"""文件传输工具核心逻辑（fs_put/fs_get/fs_stat 的实现层，纯标准库）。

让大模型在网关之间搬文件：hub 调 agent_fs_put 写本机盘，调 peer_pc2_fs_put
写对等机盘（peer 路由零改动 —— 工具注册在 agent_tools.py 的 agent FastMCP 实例上，
对等机 agent-only 模式暴露裸名 fs_put，hub 挂载时自动得 peer_<机器名>_ 前缀）。

设计约束（与需求文档一致）：
- 二进制安全：一律 'wb'/'ab' 写、'rb' 读，不做任何编码/换行转换。
- 路径归一：接受 Windows `C:\\Users\\...` 与 POSIX/MSYS `/c/Users/...` 两种写法，
  拒绝相对路径。
- 分块协议：大文件上传 put mode="append" 逐块追加；下载 get offset 逐块读；
  传输完成后调一次 fs_stat 拿整文件 sha256 终验（避免 append 每块整文件哈希的 O(n²)）。
- 错误不抛异常，返回 {ok: False, error}（模式同 host_memory.py）。

安全：与 agent_run 同信任模型（agent_run 已可在服务器执行任意命令），不做路径白名单，
靠网关 X-API-Key 兜底；写操作打 info 日志（path + bytes，不记内容）。
"""
import base64
import binascii
import hashlib
import logging
import os
import re
from pathlib import Path, PureWindowsPath
from typing import Any, Dict

from mcp_gateway.config import FS_GET_MAX_BYTES, FS_PUT_MAX_BYTES

logger = logging.getLogger("mcp_gateway.fs_tools")

# 流式哈希/读文件的块大小
_CHUNK = 1024 * 1024

# MSYS/Git-Bash 盘符路径：/c/Users/... → C:/Users/...（仅 Windows 语义下有意义）
_MSYS_DRIVE_RE = re.compile(r"^/([A-Za-z])(/|$)")


def _normalize_path(raw: str) -> Path | None:
    """归一路径；非绝对路径返回 None。

    - Windows 上把 `/c/Users/...` 归一为 `C:\\Users\\...`；`C:/...` 与 `C:\\...` 等价。
    - POSIX 上 `/home/...` 本身就是绝对路径，原样接受。
    """
    s = (raw or "").strip()
    if not s:
        return None
    if os.name == "nt":
        m = _MSYS_DRIVE_RE.match(s)
        if m:
            s = f"{m.group(1).upper()}:/{s[m.end():]}"
        # 裸 `/foo`（无盘符）在 Windows 下无明确归属，视为非法
        if not PureWindowsPath(s).drive:
            return None
    p = Path(s)
    if not p.is_absolute():
        return None
    return p.resolve()


def _sha256_file(path: Path) -> str:
    """流式计算整文件 sha256（分块读，不整读进内存）。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(_CHUNK):
            h.update(chunk)
    return h.hexdigest()


def fs_put_impl(path: str, data_b64: str, mode: str = "write",
                mkdirs: bool = True, expected_size: int = -1) -> Dict[str, Any]:
    """base64 → 主机磁盘二进制写。返回 {ok, path, bytes_written, size, sha256}。

    mode: write=覆盖截断 / append=追加（大文件分块）。
    sha256 仅 write 模式计算（写后整文件哈希）；append 模式为 None ——
    每块整文件重哈希是 O(n²)，分块上传的整文件校验走 fs_stat 一次终验。
    expected_size: 仅 append 有效（>=0 时生效）：写前校验当前文件大小须等于该值，
    不等则拒绝 —— 供调用方在网络超时重试时防止同一块被重复追加。
    """
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    if mode not in ("write", "append"):
        return {"ok": False, "error": f"mode 非法（须为 write/append）：{mode!r}"}
    try:
        data = base64.b64decode(data_b64, validate=True)
    except (binascii.Error, ValueError) as exc:
        return {"ok": False, "error": f"data_b64 非法 base64：{exc}"}
    if len(data) > FS_PUT_MAX_BYTES:
        return {"ok": False,
                "error": f"单次写入 {len(data)} 字节超上限 {FS_PUT_MAX_BYTES}，"
                         f"请用 mode='append' 分块上传"}
    try:
        if mkdirs:
            p.parent.mkdir(parents=True, exist_ok=True)
        if mode == "append" and expected_size >= 0:
            current = p.stat().st_size if p.exists() else 0
            if current != expected_size:
                return {"ok": False, "size": current,
                        "error": f"expected_size 不匹配：当前文件 {current} 字节，"
                                 f"期望 {expected_size}（可能是重试导致的重复追加，"
                                 f"请按 size 重新对齐分块）"}
        with open(p, "wb" if mode == "write" else "ab") as f:
            f.write(data)
        size = p.stat().st_size
    except OSError as exc:
        return {"ok": False, "error": f"写入失败：{exc}"}
    result: Dict[str, Any] = {"ok": True, "path": str(p),
                              "bytes_written": len(data), "size": size,
                              "sha256": None}
    if mode == "write":
        # 哈希失败不推翻已成功的写入：ok 仍为 True，sha256=None + warning，
        # 调用方可改用 fs_stat 重试校验。
        try:
            result["sha256"] = _sha256_file(p)
        except OSError as exc:
            result["warning"] = f"写入成功但哈希计算失败：{exc}"
    logger.info("fs_put %s mode=%s bytes=%d size=%d", p, mode, len(data), size)
    return result


def fs_get_impl(path: str, offset: int = 0, max_bytes: int = 0) -> Dict[str, Any]:
    """主机磁盘 → base64 二进制读。返回 {ok, path, size, offset, bytes_read, eof, sha256, data_b64}。

    offset 支持大文件分块下载；sha256 为**本块数据**的哈希，整文件校验用 fs_stat。
    max_bytes 缺省/0 即用上限 FS_GET_MAX_BYTES，超上限压回上限，负数拒绝。
    """
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    if offset < 0:
        return {"ok": False, "error": f"offset 非法（须 >= 0）：{offset}"}
    if max_bytes < 0:
        return {"ok": False, "error": f"max_bytes 非法（须 >= 0，0=用服务端上限）：{max_bytes}"}
    limit = max_bytes if 0 < max_bytes <= FS_GET_MAX_BYTES else FS_GET_MAX_BYTES
    try:
        size = p.stat().st_size
        with open(p, "rb") as f:
            f.seek(offset)
            data = f.read(limit)
    except OSError as exc:
        return {"ok": False, "error": f"读取失败：{exc}"}
    return {"ok": True, "path": str(p), "size": size, "offset": offset,
            "bytes_read": len(data), "eof": offset + len(data) >= size,
            "sha256": hashlib.sha256(data).hexdigest(),
            "data_b64": base64.b64encode(data).decode("ascii")}


def fs_stat_impl(path: str) -> Dict[str, Any]:
    """整文件校验：返回 {ok, path, size, sha256}（流式哈希，任意大小）。"""
    p = _normalize_path(path)
    if p is None:
        return {"ok": False, "error": f"path 非法（须为绝对路径）：{path!r}"}
    try:
        size = p.stat().st_size
        sha256 = _sha256_file(p)
    except OSError as exc:
        return {"ok": False, "error": f"读取失败：{exc}"}
    return {"ok": True, "path": str(p), "size": size, "sha256": sha256}
