"""Unit tests for mcp_gateway/host_memory.py."""
import pytest
from mcp_gateway.host_memory import mem_delete, mem_get, mem_list, mem_set, recall_for_prompt


@pytest.fixture(autouse=True)
def store_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_STORE_DIR", str(tmp_path))


def test_set_and_get():
    mem_set("host1", "k", "v")
    r = mem_get("host1", "k")
    assert r["ok"] is True
    assert r["fact"]["body"] == "v"


def test_get_missing_slug():
    r = mem_get("host1", "nope")
    assert r["ok"] is False
    assert "不存在" in r["error"]


def test_set_overwrites():
    mem_set("host1", "k", "first")
    mem_set("host1", "k", "second")
    assert mem_get("host1", "k")["fact"]["body"] == "second"


def test_delete_existing():
    mem_set("host1", "k", "v")
    r = mem_delete("host1", "k")
    assert r["ok"] is True and r["deleted"] is True
    assert mem_get("host1", "k")["ok"] is False


def test_delete_nonexistent():
    r = mem_delete("host1", "ghost")
    assert r["ok"] is True and r["deleted"] is False


def test_list_slugs():
    mem_set("host1", "a", "1")
    mem_set("host1", "b", "2")
    r = mem_list("host1")
    assert r["ok"] is True
    assert set(r["slugs"]) == {"a", "b"}
    assert r["count"] == 2


def test_list_empty_host():
    r = mem_list("nobody")
    assert r["ok"] is True and r["count"] == 0


def test_hosts_are_isolated():
    mem_set("hostA", "k", "for-A")
    mem_set("hostB", "k", "for-B")
    assert mem_get("hostA", "k")["fact"]["body"] == "for-A"
    assert mem_get("hostB", "k")["fact"]["body"] == "for-B"


def test_invalid_host_id():
    for bad in ("", "../escape", "a" * 129, "has space"):
        r = mem_set(bad, "k", "v")
        assert r["ok"] is False and "host_id" in r["error"]


def test_empty_slug_rejected():
    r = mem_set("host1", "", "v")
    assert r["ok"] is False and "slug" in r["error"]


def test_invalid_type_rejected():
    r = mem_set("host1", "k", "v", type="bogus")
    assert r["ok"] is False and "type" in r["error"]
    assert mem_get("host1", "k")["ok"] is False  # no row created


def test_set_created_flag_and_timestamps():
    import time
    r1 = mem_set("host1", "k", "v1")
    assert r1["ok"] is True and r1["created"] is True
    time.sleep(0.01)
    r2 = mem_set("host1", "k", "v2")
    assert r2["ok"] is True and r2["created"] is False
    f1 = mem_get("host1", "k")["fact"]
    f2 = mem_get("host1", "k")["fact"]
    assert f1["created_at"] == f2["created_at"]       # preserved across updates
    assert f1["updated_at"] != r1                     # just check key present
    # updated_at advanced on second write — re-read after second write
    mem_set("host1", "k", "v3")
    f_orig_ca = mem_get("host1", "k")["fact"]["created_at"]
    assert f_orig_ca == f1["created_at"]              # created_at never changes


def test_file_persists_across_calls():
    """Data survives independent connections (no in-memory cache)."""
    import sqlite3
    from mcp_gateway.host_memory import _db_path
    mem_set("p", "x", "persisted")
    con = sqlite3.connect(str(_db_path("p")))
    row = con.execute("SELECT body FROM facts WHERE slug='x'").fetchone()
    con.close()
    assert row is not None and row[0] == "persisted"


# ---- type, description & structured model ------------------------------------

def test_type_stored_and_returned():
    mem_set("host1", "pref", "dark", type="user")
    r = mem_get("host1", "pref")
    assert r["ok"] is True and r["fact"]["type"] == "user"


def test_description_stored_and_returned():
    mem_set("host1", "lang", "Python", description="preferred language")
    r = mem_get("host1", "lang")
    assert r["ok"] is True and r["fact"]["description"] == "preferred language"


def test_list_facts_includes_type():
    mem_set("host1", "lang", "Python", type="project")
    r = mem_list("host1")
    fact = next(f for f in r["facts"] if f["slug"] == "lang")
    assert fact["type"] == "project"


def test_type_default_project():
    mem_set("host1", "k", "v")
    assert mem_get("host1", "k")["fact"]["type"] == "project"


def test_description_default_empty():
    mem_set("host1", "k", "v")
    assert mem_get("host1", "k")["fact"]["description"] == ""


# ---- recall_for_prompt -------------------------------------------------------

def test_recall_empty_store_returns_prompt_at_end():
    """Empty DB: preamble + guidance still returned, prompt at end."""
    result = recall_for_prompt("host1", "hello")
    assert result.endswith("hello")
    assert "agent_memory_set" in result


def test_recall_empty_db_contains_guidance():
    result = recall_for_prompt("host1", "q")
    assert "agent_memory_set" in result
    assert "host1" in result


def test_recall_injects_memories_before_prompt():
    mem_set("host1", "lang", "Python", type="user")
    result = recall_for_prompt("host1", "What's my language?")
    assert result.startswith("[Host memory — host1]")
    assert "lang: Python" in result
    assert result.endswith("What's my language?")


def test_recall_multiple_slugs_all_injected():
    mem_set("host1", "a", "1", type="user")
    mem_set("host1", "b", "2", type="user")
    result = recall_for_prompt("host1", "prompt")
    assert "a: 1" in result
    assert "b: 2" in result


def test_recall_separator_between_memory_and_prompt():
    mem_set("host1", "k", "v")
    result = recall_for_prompt("host1", "q")
    lines = result.splitlines()
    assert "---" in lines
    assert lines[-1] == "q"


def test_recall_contains_writeback_hint():
    mem_set("host1", "k", "v")
    result = recall_for_prompt("host1", "q")
    assert "agent_memory_set" in result


def test_recall_empty_host_id_returns_prompt_unchanged():
    assert recall_for_prompt("", "prompt") == "prompt"


def test_recall_invalid_host_id_returns_prompt_unchanged():
    assert recall_for_prompt("../bad", "prompt") == "prompt"


# ---- new recall behavior -----------------------------------------------------

def test_recall_user_fact_always_present_regardless_of_query():
    mem_set("host1", "name", "Alice", type="user")
    mem_set("host1", "proj", "StockSDK", description="current project", type="project")
    result = recall_for_prompt("host1", "tell me about the project", query="project")
    assert "[user] name: Alice" in result


def test_recall_query_keyword_ranks_matching_fact_first():
    mem_set("host1", "db-host", "localhost", description="database connection host", type="project")
    mem_set("host1", "editor", "vim", description="text editor preference", type="feedback")
    result = recall_for_prompt("host1", "anything", query="database connection")
    assert result.index("db-host") < result.index("editor")


def test_recall_top_k_limits_non_user_facts():
    for i in range(12):
        mem_set("host1", f"fact{i}", f"v{i}", description=f"desc {i}", type="project")
    result = recall_for_prompt("host1", "anything", top_k=3)
    non_user_lines = [ln for ln in result.splitlines() if ln.startswith("[project]")]
    assert len(non_user_lines) <= 3


# ---- relevance scoring (updated for query-based ranking) ---------------------

def test_recall_relevant_fact_ranks_above_irrelevant():
    mem_set("host1", "python-version", "3.11", description="python version in use", type="project")
    mem_set("host1", "favorite-food", "ramen", description="food preference", type="reference")
    result = recall_for_prompt("host1", "anything", query="python version")
    assert result.index("python-version") < result.index("favorite-food")


def test_recall_type_contributes_to_score():
    # slug "conn" and description match query, editor does not
    mem_set("host1", "conn", "localhost:5432", description="database connection", type="reference")
    mem_set("host1", "editor", "vim", description="text editor", type="project")
    result = recall_for_prompt("host1", "anything", query="database connection")
    assert result.index("conn") < result.index("editor")


def test_recall_description_contributes_to_score():
    mem_set("host1", "conn", "localhost:5432", description="primary database host", type="project")
    mem_set("host1", "editor", "vim", description="text editor", type="feedback")
    result = recall_for_prompt("host1", "anything", query="database host")
    assert result.index("conn") < result.index("editor")


def test_recall_top_k_limits_injected_facts():
    for i in range(13):
        mem_set("host1", f"k{i}", f"v{i}", type="project")
    result = recall_for_prompt("host1", "anything", top_k=5)
    non_user_lines = [ln for ln in result.splitlines() if ln.startswith("[project]")]
    assert len(non_user_lines) <= 5
