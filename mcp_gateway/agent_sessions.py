"""服务器端 Agent 会话列表（agent_sessions 工具，仿原生 /resume）。

CLI 本身不暴露 list 子命令；两个引擎都把会话存成可扫描的 JSONL，本模块**纯读扫盘**，
按当前 project cwd 过滤，派生人类可读标题，按修改时间倒序、限量返回：

  claude: ~/.claude/projects/<编码cwd>/<uuid>.jsonl       （文件名 stem 即 session_id）
  codex:  ~/.codex/sessions/YYYY/MM/DD/rollout-*-<uuid>.jsonl  （首行 session_meta.payload.id）

标题与原生 /resume 兜底一致：取第一条「非 <...> 标签 / 非 command-name / 非 caveat」的
user 文本，截断；取不到 → "(无标题) {modified}"。

健壮性：单文件读失败 / JSON 坏行 → 跳过该文件（debug），绝不让整列表崩；目录不存在 → 空列表。
性能：每源先按 mtime 取最新前 2*limit 个文件再派生标题；标题读到首条命中即 break，不整文件载入。
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from mcp_gateway.config import (
    AGENT_SESSION_TITLE_MAXLEN,
    encode_claude_project_dir,
    get_claude_projects_dir,
    get_codex_sessions_dir,
)

logger = logging.getLogger("mcp_gateway.agent_sessions")

_NO_TITLE = "(无标题)"


def list_sessions(cwd: str, limit: int) -> List[Dict[str, object]]:
    """列出本项目（cwd）下 claude + codex 历史会话，按 mtime 倒序，截 limit。

    每条：{session_id, engine, title, mtime(float), modified(ISO 字符串)}。
    """
    sessions = _list_claude(cwd, limit) + _list_codex(cwd, limit)
    sessions.sort(key=lambda s: s["mtime"], reverse=True)
    return sessions[:limit]


# ---- claude ----------------------------------------------------------------

def _list_claude(cwd: str, limit: int) -> List[Dict[str, object]]:
    """扫 ~/.claude/projects/<编码cwd>/*.jsonl。文件名 stem 即 session_id。"""
    proj_dir = get_claude_projects_dir() / encode_claude_project_dir(cwd)
    if not proj_dir.is_dir():
        return []
    out: List[Dict[str, object]] = []
    for f in _newest_files(proj_dir.glob("*.jsonl"), limit):
        try:
            mtime = f.stat().st_mtime
        except OSError:
            continue
        title = _derive_title(f, _claude_user_text) or _untitled(mtime)
        out.append(_entry(f.stem, "claude", title, mtime))
    return out


def _claude_user_text(obj: dict) -> Optional[str]:
    """从 claude transcript 一行里取 user 消息文本（无则 None）。"""
    if obj.get("type") != "user":
        return None
    msg = obj.get("message") or {}
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text"
        )
    return None


# ---- codex -----------------------------------------------------------------

def _list_codex(cwd: str, limit: int) -> List[Dict[str, object]]:
    """扫 ~/.codex/sessions/**/rollout-*.jsonl。按首行 session_meta.payload.cwd 过滤。"""
    root = get_codex_sessions_dir()
    if not root.is_dir():
        return []
    out: List[Dict[str, object]] = []
    for f in _newest_files(root.rglob("rollout-*.jsonl"), limit):
        meta = _codex_meta(f)
        if meta is None:
            continue
        sid, file_cwd = meta
        if file_cwd != cwd:
            continue
        try:
            mtime = f.stat().st_mtime
        except OSError:
            continue
        title = _derive_title(f, _codex_user_text) or _untitled(mtime)
        out.append(_entry(sid, "codex", title, mtime))
    return out


def _codex_meta(f: Path) -> Optional[tuple]:
    """读 codex 会话首行 session_meta，返回 (session_id, cwd)；失败 None。"""
    try:
        with f.open(encoding="utf-8", errors="replace") as fh:
            first = fh.readline()
        obj = json.loads(first)
    except (OSError, ValueError):
        return None
    payload = obj.get("payload") if isinstance(obj, dict) else None
    if not isinstance(payload, dict):
        return None
    sid = payload.get("id")
    file_cwd = payload.get("cwd")
    if not isinstance(sid, str) or not sid.strip():
        return None
    return sid.strip(), file_cwd


def _codex_user_text(obj: dict) -> Optional[str]:
    """从 codex transcript 一行里取 user 消息文本（无则 None）。"""
    payload = obj.get("payload") if isinstance(obj, dict) else None
    if not isinstance(payload, dict):
        return None
    # codex 把用户输入放在 response_item / event_msg 的 payload 里，字段名跨版本有差异，
    # 这里宽松探测常见承载文本的字段。
    if payload.get("role") == "user" or payload.get("type") in ("user_message", "user_input"):
        text = payload.get("text") or payload.get("message") or payload.get("content")
        if isinstance(text, str):
            return text
        if isinstance(text, list):
            return " ".join(
                x.get("text", "") for x in text if isinstance(x, dict)
            )
    return None


# ---- 通用 -------------------------------------------------------------------

def _derive_title(f: Path, extract) -> Optional[str]:
    """流式读 transcript，取第一条有意义的用户文本作标题（截断）。

    extract(obj) 引擎特定：从一行 JSON 取 user 文本或 None。读到首条命中即 break。
    单文件读失败 / 坏行 → 返回 None（调用方用 mtime 兜底）。
    """
    try:
        with f.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (ValueError, TypeError):
                    continue
                text = extract(obj)
                if text is None:
                    continue
                cleaned = _clean_title(text)
                if cleaned:
                    return cleaned
    except OSError:
        logger.debug("读会话文件失败，跳过标题派生：%s", f)
    return None


def _clean_title(text: str) -> Optional[str]:
    """把用户文本清成标题：跳过标签/命令/caveat，strip + 截断。无意义 → None。"""
    text = (text or "").strip()
    if not text:
        return None
    # 跳过 <...> 标签开头（command-name / local-command-caveat / system-reminder 等）
    if text.startswith("<"):
        return None
    head = text[:60].lower()
    if "command-name" in head or "caveat" in head or "command-message" in head:
        return None
    # 单行化 + 截断
    title = " ".join(text.split())
    if len(title) > AGENT_SESSION_TITLE_MAXLEN:
        title = title[:AGENT_SESSION_TITLE_MAXLEN] + "…"
    return title or None


def _newest_files(paths, limit: int) -> List[Path]:
    """按 mtime 倒序取最新前 2*limit 个文件（限制要派生标题的文件数）。"""
    files = [p for p in paths if p.is_file()]
    cap = max(limit * 2, limit)

    def _mtime(p: Path) -> float:
        try:
            return p.stat().st_mtime
        except OSError:
            return 0.0

    files.sort(key=_mtime, reverse=True)
    return files[:cap]


def _untitled(mtime: float) -> str:
    return "{} {}".format(_NO_TITLE, _iso(mtime))


def _iso(mtime: float) -> str:
    return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()


def _entry(session_id: str, engine: str, title: str, mtime: float) -> Dict[str, object]:
    return {
        "session_id": session_id,
        "engine": engine,
        "title": title,
        "mtime": mtime,
        "modified": _iso(mtime),
    }
