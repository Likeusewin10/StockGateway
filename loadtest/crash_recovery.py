"""崩溃自愈测试：杀掉服务进程，观测它是否按设计自动拉起，并量化恢复耗时。

服务有两层自愈（均已存在于仓库，本脚本只验证，不重建）：
  层一 看门狗：start_server.bat 是 `:loop` 循环，uvicorn 退出后 5s 重启
                （RESTART_DELAY_SECONDS）。
  层二 计划任务：register_task.ps1 注册 StockDataService，LogonTrigger +
                每分钟 TimeTrigger + RestartOnFailure×999，连看门狗控制台被
                关都能 1 分钟内拉起。

定位进程**按监听端口精确锁定 PID**，绝不按进程名全杀——否则会误伤 8765 的
MCP 网关（同样是 uvicorn）。优先用 psutil，缺失时回退到 netstat 解析。

用法：
    # 层一：杀 uvicorn 子进程，验证看门狗 5s 内拉起
    .venv-api\\Scripts\\python loadtest\\crash_recovery.py --layer watchdog

    # 层二：连看门狗 cmd 一起杀，验证计划任务 1 分钟内自愈（需已注册任务）
    .venv-api\\Scripts\\python loadtest\\crash_recovery.py --layer task
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

# 允许 `python loadtest/crash_recovery.py` 直接运行：把项目根放进 sys.path。
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loadtest._common import DEFAULT_PORT, RATE_LIMIT_WINDOW_SECONDS  # noqa: F401,E402
from stocksdk.config import RESTART_DELAY_SECONDS  # noqa: E402

TASK_NAME = "StockDataService"


# ---------- 端口 → PID 定位（psutil 优先，netstat 回退） ----------

def _pids_listening_psutil(port: int) -> list[int]:
    import psutil
    pids: list[int] = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            if conn.pid:
                pids.append(conn.pid)
    return sorted(set(pids))


def _pids_listening_netstat(port: int) -> list[int]:
    """无 psutil 时回退：netstat -ano 找 LISTENING 行末的 PID。"""
    out = subprocess.run(
        ["netstat", "-ano", "-p", "TCP"],
        capture_output=True, text=True, check=False,
    ).stdout
    pids: list[int] = []
    for line in out.splitlines():
        if "LISTENING" not in line:
            continue
        # 形如：  TCP    0.0.0.0:8000   0.0.0.0:0   LISTENING   12345
        m = re.search(r":(\d+)\s+\S+\s+LISTENING\s+(\d+)", line)
        if m and int(m.group(1)) == port:
            pids.append(int(m.group(2)))
    return sorted(set(pids))


def pids_listening(port: int) -> list[int]:
    try:
        import psutil  # noqa: F401
        return _pids_listening_psutil(port)
    except ImportError:
        return _pids_listening_netstat(port)


def _proc_name(pid: int) -> str:
    try:
        import psutil
        return psutil.Process(pid).name()
    except Exception:
        return "?"


def _parent_chain(pid: int) -> list[int]:
    """从 pid 向上取父进程链（用于层二杀看门狗 cmd）。需 psutil。"""
    chain: list[int] = []
    try:
        import psutil
        p = psutil.Process(pid)
        while p is not None:
            try:
                parent = p.parent()
            except Exception:
                break
            if parent is None:
                break
            chain.append(parent.pid)
            name = parent.name().lower()
            # 看门狗是 cmd.exe 跑 start_server.bat；到 cmd 即停。
            if "cmd" in name:
                break
            p = parent
    except Exception:
        pass
    return chain


def kill_pid(pid: int) -> None:
    """强杀单个 PID。psutil 优先，回退 taskkill。"""
    try:
        import psutil
        psutil.Process(pid).kill()
        return
    except ImportError:
        pass
    except Exception:
        pass
    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                   capture_output=True, check=False)


# ---------- 探活 ----------

def health_ok(port: int, timeout: float = 2.0) -> bool:
    url = "http://127.0.0.1:{}/health".format(port)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def wait_until(predicate, timeout_s: float, poll_s: float = 0.5) -> float | None:
    """轮询 predicate 直到为真或超时。返回耗时秒，超时返回 None。"""
    start = time.monotonic()
    deadline = start + timeout_s
    while time.monotonic() < deadline:
        if predicate():
            return time.monotonic() - start
        time.sleep(poll_s)
    return None


# ---------- 计划任务状态 ----------

def task_registered(name: str = TASK_NAME) -> bool:
    r = subprocess.run(["schtasks", "/Query", "/TN", name],
                       capture_output=True, text=True, check=False)
    return r.returncode == 0


# ---------- 两层测试 ----------

def run_watchdog_layer(port: int, recover_timeout: float) -> int:
    """层一：只杀 uvicorn 子进程，看门狗应在 RESTART_DELAY_SECONDS 余量内拉起。"""
    print("== 层一：看门狗 (start_server.bat 循环) ==")
    if not health_ok(port):
        print("✗ 服务当前未在 :{} 响应 /health，无法测试。先启动服务。".format(port))
        return 2
    pids = pids_listening(port)
    if not pids:
        print("✗ 未在 :{} 找到 LISTENING 进程（端口被代理转发？）。".format(port))
        return 2
    print("命中监听 :{} 的 PID：{}（{}）".format(
        port, pids, ", ".join(_proc_name(p) for p in pids)))
    for pid in pids:
        print("  kill {} ...".format(pid))
        kill_pid(pid)

    # 先确认确实挂了（短暂等待端口释放）
    down = wait_until(lambda: not health_ok(port), timeout_s=10, poll_s=0.3)
    if down is None:
        print("⚠ 杀后 /health 仍可用：可能命中了错误进程，或已被瞬间拉起。")
    else:
        print("  服务已下线（{:.1f}s 后 /health 不可达）。".format(down))

    budget = RESTART_DELAY_SECONDS + 10   # 看门狗 5s + uvicorn 启动 + 首登余量
    print("  等待自愈（预算 {}s = 看门狗 {}s + 启动余量）...".format(
        budget, RESTART_DELAY_SECONDS))
    recovered = wait_until(lambda: health_ok(port), timeout_s=recover_timeout)
    if recovered is None:
        print("✗ FAIL：{}s 内未恢复。检查看门狗是否在跑"
              "（start_server.bat / 计划任务 StockDataService）。".format(
                  recover_timeout))
        return 1
    verdict = "✓ PASS" if recovered <= budget else "△ 慢"
    print("{}：{:.1f}s 后恢复（预算 {}s）。".format(verdict, recovered, budget))
    return 0


def run_task_layer(port: int, recover_timeout: float) -> int:
    """层二：杀 uvicorn 及其看门狗 cmd，验证计划任务 1 分钟兜底拉起。"""
    print("== 层二：计划任务自愈 (StockDataService 每分钟 TimeTrigger) ==")
    if not task_registered():
        print("○ SKIP：计划任务 '{}' 未注册（运行 install_service.bat 注册后再测）。"
              .format(TASK_NAME))
        return 0
    if not health_ok(port):
        print("✗ 服务当前未响应 /health，无法测试。先启动服务。")
        return 2
    pids = pids_listening(port)
    if not pids:
        print("✗ 未找到监听 :{} 的进程。".format(port))
        return 2

    # 收集 uvicorn + 其看门狗 cmd 链，一起杀，模拟「整个看门狗都没了」
    victims: set[int] = set(pids)
    for pid in pids:
        for ancestor in _parent_chain(pid):
            victims.add(ancestor)
    print("命中进程链 PID：{}".format(sorted(victims)))
    print("（含 uvicorn 与其父 cmd 看门狗；杀掉后只剩计划任务能拉起）")
    for pid in sorted(victims):
        kill_pid(pid)

    down = wait_until(lambda: not health_ok(port), timeout_s=15, poll_s=0.3)
    if down is None:
        print("⚠ 仍可用：进程链可能未杀全。")
    else:
        print("  服务已下线（{:.1f}s）。".format(down))

    # 计划任务每分钟触发，最坏需等近 1 分钟 + 启动时间
    budget = 60 + RESTART_DELAY_SECONDS + 15
    print("  等待计划任务兜底（预算约 {}s = 1 分钟 TimeTrigger + 启动）...".format(budget))
    recovered = wait_until(lambda: health_ok(port), timeout_s=recover_timeout)
    if recovered is None:
        print("✗ FAIL：{}s 内未由计划任务拉起。检查 schtasks /Query /TN {} 是否 Ready。"
              .format(recover_timeout, TASK_NAME))
        return 1
    verdict = "✓ PASS" if recovered <= budget else "△ 慢"
    print("{}：{:.1f}s 后由计划任务恢复（预算约 {}s）。".format(verdict, recovered, budget))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="崩溃自愈测试（看门狗层 / 计划任务层）")
    p.add_argument("--layer", choices=["watchdog", "task"], default="watchdog",
                   help="watchdog=只杀 uvicorn；task=连看门狗一起杀验计划任务")
    p.add_argument("--port", type=int, default=DEFAULT_PORT)
    p.add_argument("--recover-timeout", type=float, default=None,
                   help="恢复等待上限秒。默认 watchdog=30 / task=120")
    args = p.parse_args()

    timeout = args.recover_timeout
    if timeout is None:
        timeout = 30.0 if args.layer == "watchdog" else 120.0

    if sys.platform != "win32":
        print("⚠ 本脚本针对 Windows 的看门狗/计划任务；非 Windows 仅供参考。")

    if args.layer == "watchdog":
        return run_watchdog_layer(args.port, timeout)
    return run_task_layer(args.port, timeout)


if __name__ == "__main__":
    raise SystemExit(main())
