"""Per-host persistent memory: SQLite structured fact store with relevance recall.

One .db file per host under MEMORY_STORE_DIR (~/.mcp_gateway/memory/).
Facts: slug (PK), body, type, description, created_at, updated_at.
recall_for_prompt scores facts by prompt-token overlap against slug+body+type+description.
"""
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Generator, Optional

_VALID_HOST_ID = re.compile(r"^[a-zA-Z0-9._-]{1,128}$")

_DDL = (
    "CREATE TABLE IF NOT EXISTS facts ("
    "  slug        TEXT PRIMARY KEY NOT NULL,"
    "  body        TEXT NOT NULL DEFAULT '',"
    "  type        TEXT NOT NULL DEFAULT 'project',"
    "  description TEXT NOT NULL DEFAULT '',"
    "  created_at  TEXT NOT NULL,"
    "  updated_at  TEXT NOT NULL"
    ")"
)

RECALL_TOP_K = 10
_VALID_TYPES = {"user", "project", "feedback", "reference"}


def get_memory_store_dir() -> Path:
    raw = os.environ.get("MEMORY_STORE_DIR", "").strip()
    return Path(raw) if raw else Path.home() / ".mcp_gateway" / "memory"


def _db_path(host_id: str) -> Path:
    return get_memory_store_dir() / f"{host_id}.db"


@contextmanager
def _db(host_id: str) -> Generator[sqlite3.Connection, None, None]:
    p = _db_path(host_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(p))
    con.execute("PRAGMA journal_mode=WAL")
    con.execute(_DDL)
    con.commit()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def _validate(host_id: str) -> Optional[str]:
    if not _VALID_HOST_ID.match(host_id or ""):
        return "host_id 非法（限1-128位字母数字及 - _ .）"
    return None


def mem_set(host_id: str, slug: str, body: str, *,
            description: str = "", type: str = "project") -> Dict[str, Any]:
    if err := _validate(host_id):
        return {"ok": False, "error": err}
    if not slug:
        return {"ok": False, "error": "slug 不能为空"}
    if type not in _VALID_TYPES:
        return {"ok": False, "error": f"type 非法，须为 {sorted(_VALID_TYPES)} 之一"}
    now = datetime.now(timezone.utc).isoformat()
    with _db(host_id) as con:
        exists = con.execute(
            "SELECT 1 FROM facts WHERE slug=?", (slug,)
        ).fetchone() is not None
        con.execute(
            "INSERT INTO facts(slug,body,type,description,created_at,updated_at)"
            " VALUES(?,?,?,?,?,?)"
            " ON CONFLICT(slug) DO UPDATE SET body=excluded.body,type=excluded.type,"
            "description=excluded.description,updated_at=excluded.updated_at",
            (slug, body, type, description, now, now),
        )
    return {"ok": True, "host_id": host_id, "slug": slug, "created": not exists}


def mem_get(host_id: str, slug: str) -> Dict[str, Any]:
    if err := _validate(host_id):
        return {"ok": False, "error": err}
    with _db(host_id) as con:
        row = con.execute(
            "SELECT body, type, description, created_at, updated_at FROM facts WHERE slug=?",
            (slug,),
        ).fetchone()
    if row is None:
        return {"ok": False, "error": f"slug '{slug}' 不存在"}
    return {"ok": True, "fact": {
        "slug": slug, "description": row[2], "body": row[0],
        "type": row[1], "created_at": row[3], "updated_at": row[4],
    }}


def mem_delete(host_id: str, slug: str) -> Dict[str, Any]:
    if err := _validate(host_id):
        return {"ok": False, "error": err}
    with _db(host_id) as con:
        deleted = con.execute("DELETE FROM facts WHERE slug=?", (slug,)).rowcount > 0
    return {"ok": True, "host_id": host_id, "slug": slug, "deleted": deleted}


def mem_list(host_id: str) -> Dict[str, Any]:
    if err := _validate(host_id):
        return {"ok": False, "error": err}
    with _db(host_id) as con:
        rows = con.execute(
            "SELECT slug, type, description, updated_at FROM facts ORDER BY updated_at DESC"
        ).fetchall()
    facts = [{"slug": r[0], "type": r[1], "description": r[2], "updated_at": r[3]}
             for r in rows]
    return {"ok": True, "host_id": host_id,
            "slugs": [f["slug"] for f in facts], "facts": facts, "count": len(facts)}


def _tokenize(text: str) -> set:
    """Lowercase tokens: ASCII words ≥2 chars + individual CJK chars."""
    return {w for w in re.findall(r"[a-z]{2,}|[一-鿿]", text.lower())}


def _score(tokens: set, slug: str, body: str, type: str, description: str) -> int:
    blob = f"{slug} {body} {type} {description}".lower()
    return sum(1 for t in tokens if t in blob)


def recall_for_prompt(host_id: str, prompt: str, query: str = "", top_k: int = 8) -> str:
    """Prefix prompt with structured memory preamble; unchanged if invalid host."""
    if not host_id or _validate(host_id):
        return prompt
    with _db(host_id) as con:
        rows = con.execute(
            "SELECT slug, body, type, description, updated_at FROM facts"
            " ORDER BY updated_at DESC"
        ).fetchall()

    user_facts = [r for r in rows if r[2] == "user"]
    non_user = [r for r in rows if r[2] != "user"]

    if query.strip():
        kws = [k.lower() for k in query.split()]
        def _match(r: tuple) -> bool:
            blob = (r[0] + " " + r[3]).lower()
            return any(k in blob for k in kws)
        non_user_ordered = [r for r in non_user if _match(r)] + \
                           [r for r in non_user if not _match(r)]
    else:
        non_user_ordered = non_user

    selected = non_user_ordered[:top_k]

    guidance = (
        f"可调用 agent_memory_set(host_id='{host_id}', slug=..., body=..., "
        "description=..., type=...) 记录长期事实，"
        "type 取值：user/project/feedback/reference。"
    )

    header = f"[Host memory — {host_id}]"
    user_lines = [f"[user] {r[0]}: {r[1]}" for r in user_facts]
    non_user_lines = [f"[{r[2]}] {r[0]} - {r[3]}" for r in selected]

    preamble = "\n".join([header] + user_lines + non_user_lines + [guidance])

    if len(preamble) > 4000:
        non_user_lines = [f"[{r[2]}] {r[0]}" for r in selected]
        preamble = "\n".join([header] + user_lines + non_user_lines + [guidance])

    return f"{preamble}\n---\n{prompt}"
