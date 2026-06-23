"""会话列表单测（mcp_gateway/agent_sessions.py）。

用 monkeypatch.setenv 把 CLAUDE_PROJECTS_DIR / CODEX_SESSIONS_DIR 指向 tmp_path，
造假 transcript，不触发真实磁盘会话。覆盖：claude 标题派生 + session_id=文件名、
codex 按 cwd 过滤、标题跳过命令/caveat 行、按 mtime 倒序限量、坏 JSON 跳过、缺目录空列表。
"""
import json
import os

import pytest

from mcp_gateway.agent_sessions import list_sessions
from mcp_gateway.config import encode_claude_project_dir

CWD = r"D:\dev\Project\StockSDK"
OTHER_CWD = r"D:\dev\Project\other"


@pytest.fixture
def session_dirs(tmp_path, monkeypatch):
    """把两个会话根指向 tmp 子目录，返回 (claude_proj_dir, codex_root)。"""
    claude_root = tmp_path / "claude_projects"
    codex_root = tmp_path / "codex_sessions"
    monkeypatch.setenv("CLAUDE_PROJECTS_DIR", str(claude_root))
    monkeypatch.setenv("CODEX_SESSIONS_DIR", str(codex_root))
    claude_proj = claude_root / encode_claude_project_dir(CWD)
    claude_proj.mkdir(parents=True)
    codex_root.mkdir(parents=True)
    return claude_proj, codex_root


def _write_claude(proj_dir, session_id, lines, mtime=None):
    """写一个 claude transcript（文件名即 session_id）。lines 为 dict 列表。"""
    f = proj_dir / "{}.jsonl".format(session_id)
    f.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines), encoding="utf-8")
    if mtime is not None:
        os.utime(f, (mtime, mtime))
    return f


def _claude_user(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def _write_codex(codex_root, session_id, cwd, user_text=None, mtime=None):
    """写一个 codex rollout transcript（首行 session_meta）。"""
    day = codex_root / "2026" / "06" / "23"
    day.mkdir(parents=True, exist_ok=True)
    f = day / "rollout-2026-06-23T10-00-00-{}.jsonl".format(session_id)
    lines = [{"type": "session_meta", "payload": {"id": session_id, "cwd": cwd}}]
    if user_text is not None:
        lines.append({"type": "response_item", "payload": {"role": "user", "text": user_text}})
    f.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in lines), encoding="utf-8")
    if mtime is not None:
        os.utime(f, (mtime, mtime))
    return f


def test_claude_session_listed_with_derived_title(session_dirs):
    claude_proj, _ = session_dirs
    sid = "4b167ebd-0b3d-4488-bf3f-a160b9bb8dc3"
    _write_claude(claude_proj, sid, [_claude_user("帮我列出当前目录")], mtime=1000)

    rows = list_sessions(CWD, 30)

    assert len(rows) == 1
    assert rows[0]["session_id"] == sid
    assert rows[0]["engine"] == "claude"
    assert rows[0]["title"] == "帮我列出当前目录"


def test_codex_session_filtered_by_cwd(session_dirs):
    _, codex_root = session_dirs
    _write_codex(codex_root, "019edfbc-1784-7902-b0ca-39c61d53f0bf", CWD, "本项目的问题", mtime=2000)
    _write_codex(codex_root, "019edfbc-1784-7902-b0ca-000000000000", OTHER_CWD, "别项目", mtime=2001)

    rows = list_sessions(CWD, 30)

    assert len(rows) == 1
    assert rows[0]["session_id"] == "019edfbc-1784-7902-b0ca-39c61d53f0bf"
    assert rows[0]["title"] == "本项目的问题"


def test_title_skips_command_and_caveat_lines(session_dirs):
    claude_proj, _ = session_dirs
    sid = "11111111-1111-1111-1111-111111111111"
    _write_claude(claude_proj, sid, [
        _claude_user("<local-command-caveat>Caveat: ...</local-command-caveat>"),
        _claude_user("<command-name>/plan</command-name>"),
        _claude_user("这才是真正的问题"),
    ], mtime=1000)

    rows = list_sessions(CWD, 30)

    assert rows[0]["title"] == "这才是真正的问题"


def test_sorted_by_mtime_desc_and_limited(session_dirs):
    claude_proj, _ = session_dirs
    for i in range(5):
        sid = "00000000-0000-0000-0000-00000000000{}".format(i)
        _write_claude(claude_proj, sid, [_claude_user("会话 {}".format(i))], mtime=1000 + i)

    rows = list_sessions(CWD, 3)

    assert len(rows) == 3
    # mtime 倒序：最新(i=4)在前
    assert rows[0]["title"] == "会话 4"
    assert rows[1]["title"] == "会话 3"
    assert rows[2]["title"] == "会话 2"


def test_corrupt_jsonl_skipped(session_dirs):
    claude_proj, _ = session_dirs
    good = "22222222-2222-2222-2222-222222222222"
    bad = "33333333-3333-3333-3333-333333333333"
    _write_claude(claude_proj, good, [_claude_user("好会话")], mtime=1000)
    # 坏文件：非法 JSON 行 + 无可用标题，但不能让整列表崩
    (claude_proj / "{}.jsonl".format(bad)).write_text("{not valid json\n", encoding="utf-8")
    os.utime(claude_proj / "{}.jsonl".format(bad), (1001, 1001))

    rows = list_sessions(CWD, 30)

    ids = {r["session_id"] for r in rows}
    assert good in ids                       # 好会话照常返回
    # 坏文件仍登记(session_id=文件名)但标题回退"(无标题)"，不崩
    bad_row = next((r for r in rows if r["session_id"] == bad), None)
    assert bad_row is not None
    assert "无标题" in bad_row["title"]


def test_missing_dirs_return_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECTS_DIR", str(tmp_path / "nope_claude"))
    monkeypatch.setenv("CODEX_SESSIONS_DIR", str(tmp_path / "nope_codex"))

    assert list_sessions(CWD, 30) == []


def test_claude_and_codex_merged_and_sorted(session_dirs):
    claude_proj, codex_root = session_dirs
    _write_claude(claude_proj, "44444444-4444-4444-4444-444444444444",
                  [_claude_user("claude 较旧")], mtime=1000)
    _write_codex(codex_root, "019edfbc-1784-7902-b0ca-39c61d53f0bf", CWD,
                 "codex 较新", mtime=3000)

    rows = list_sessions(CWD, 30)

    assert len(rows) == 2
    assert rows[0]["engine"] == "codex"      # 较新在前
    assert rows[1]["engine"] == "claude"
