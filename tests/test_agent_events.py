"""Unit tests for the streaming events feature."""
import pytest

import mcp_gateway.agent_runner as agent_runner
from mcp_gateway.agent_runner import AgentTask, AgentRunner, _build_command


class FakeProc:
    def __init__(self, stdout_lines, returncode=0):
        self.returncode = returncode
        self.stdout = iter(stdout_lines)
        self.stderr = iter([])

    def wait(self, timeout=None):
        return self.returncode

    def kill(self):
        pass


def test_append_event_increments_seq():
    task = AgentTask(task_id="t1", engine="claude", prompt="p")
    task.append_event({"type": "a"})
    task.append_event({"type": "b"})
    task.append_event({"type": "c"})
    assert task.event_seq == 3
    assert [ev["seq"] for ev in task.events] == [1, 2, 3]


def test_append_event_evicts_and_counts_dropped(monkeypatch):
    monkeypatch.setattr(agent_runner, "AGENT_EVENT_BUFFER_MAX", 2)
    task = AgentTask(task_id="t1", engine="claude", prompt="p")
    for i in range(5):
        task.append_event({"type": str(i)})
    assert len(task.events) == 2
    assert task.dropped == 3
    assert [ev["seq"] for ev in task.events] == [4, 5]


def test_snapshot_filters_by_cursor():
    task = AgentTask(task_id="t1", engine="claude", prompt="p")
    task.append_event({"type": "a"})
    task.append_event({"type": "b"})
    task.append_event({"type": "c"})
    snap = task.snapshot_events(1)
    assert len(snap["events"]) == 2
    assert all(ev["seq"] > 1 for ev in snap["events"])
    assert snap["next_cursor"] == 3
    assert snap["dropped"] == 0
    assert "task_id" in snap
    assert "status" in snap


def test_snapshot_cursor_at_end_empty():
    task = AgentTask(task_id="t1", engine="claude", prompt="p")
    task.append_event({"type": "a"})
    task.append_event({"type": "b"})
    snap = task.snapshot_events(2)
    assert snap["events"] == []
    assert snap["next_cursor"] == 2


def test_runner_events_unknown():
    runner = AgentRunner()
    result = runner.events("nope")
    assert result["status"] == "unknown"
    assert result["task_id"] == "nope"


def test_runner_events_known():
    runner = AgentRunner()
    task = AgentTask(task_id="k1", engine="claude", prompt="p")
    runner._store(task)
    task.append_event({"type": "a"})
    result = runner.events("k1", 0)
    assert len(result["events"]) == 1
    assert result["next_cursor"] == 1
    assert result["status"] == task.status


def test_build_command_claude_stream_true():
    cmd = _build_command("claude", "p", "claude.exe", "s", False, True)
    assert "stream-json" in cmd
    assert "--verbose" in cmd


def test_build_command_claude_stream_false():
    cmd = _build_command("claude", "p", "claude.exe", "s", False, False)
    assert "json" in cmd
    assert "stream-json" not in cmd


def test_build_command_codex_stream_true_falls_back():
    cmd = _build_command("codex", "p", "codex.exe", None, False, True)
    assert "stream-json" not in cmd


def test_pop_pending_priority():
    task = AgentTask(task_id="p1", engine="claude", prompt="p")
    task.enqueue_send("a", 0)
    task.enqueue_send("b", 5)
    task.enqueue_send("c", 0)
    order = [task.pop_pending()["text"] for _ in range(3)]
    assert order == ["b", "a", "c"]


def test_send_unknown():
    runner = AgentRunner()
    result = runner.send("nope", "any message")
    assert result["ok"] is False
    assert result["status"] == "unknown"


def test_send_not_live():
    runner = AgentRunner()
    task = AgentTask(task_id="n1", engine="claude", prompt="p", live=False)
    runner._store(task)
    result = runner.send("n1", "a message")
    assert result["ok"] is False
    assert "not a live session" in result["error"]


def test_send_and_close_live():
    runner = AgentRunner()
    task = AgentTask(task_id="l1", engine="claude", prompt="p", live=True)
    runner._store(task)
    result = runner.send("l1", "hi", 0)
    assert result["ok"] is True
    assert result["queued"] == 1
    assert len(task.pending) == 1
    closed = runner.close("l1")
    assert closed["ok"] is True
    assert task.close_requested is True


def test_wait_stream_happy_path():
    runner = AgentRunner()
    task = AgentTask(task_id="w1", engine="claude", prompt="p", stream=True)
    task._proc = FakeProc([
        '{"type": "system"}',
        '{"type": "assistant"}',
        '{"type": "result", "result": "done"}',
    ])
    runner._wait_stream(task)
    assert task.status == agent_runner.STATUS_DONE
    assert task.returncode == 0
    assert len(task.events) == 3
    assert task.event_seq == 3
    assert "result" in task.output
