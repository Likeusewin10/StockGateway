"""PoC: does claude persistent stdin streaming multi-turn work on this Windows host?

Probes the known second-message hang: drives a single long-lived claude process
over stream-json stdin/stdout for two user turns and reports whether turn two
ever produces a result envelope. ASCII-only output.
"""
import json
import os
import queue
import shutil
import subprocess
import threading
import time


FLAGS = [
    "-p",
    "--input-format", "stream-json",
    "--output-format", "stream-json",
    "--verbose",
    "--dangerously-skip-permissions",
]


def _user_turn(text):
    return {
        "type": "user",
        "message": {"role": "user", "content": [{"type": "text", "text": text}]},
    }


def main():
    exe = shutil.which("claude")
    if exe is None:
        print("[fail] claude not found on PATH")
        return

    proc = subprocess.Popen(
        [exe] + FLAGS,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        cwd=os.getcwd(),
    )

    q = queue.Queue()

    def _reader():
        for line in proc.stdout:
            q.put(line)
        q.put(None)

    threading.Thread(target=_reader, daemon=True).start()

    def send(obj):
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()

    def read_until_result(timeout):
        deadline = time.monotonic() + timeout
        types = []
        retry_flag = False
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return "timeout", types, retry_flag
            try:
                line = q.get(timeout=remaining)
            except queue.Empty:
                return "timeout", types, retry_flag
            if line is None:
                return "eof", types, retry_flag
            text = line.strip()
            if not text:
                continue
            try:
                obj = json.loads(text)
            except Exception:
                continue
            t = obj.get("type", "")
            types.append(t)
            if t == "system" and obj.get("subtype") == "api_retry":
                retry_flag = True
            if t == "result":
                return obj.get("result", ""), types, retry_flag

    def cleanup():
        try:
            proc.stdin.close()
        except Exception:
            pass
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        print("returncode=" + str(proc.returncode))

    print("--- turn one ---")
    send(_user_turn("Reply with exactly the letter A and nothing else."))
    outcome1, types1, retry1 = read_until_result(180)
    print("turn one outcome=" + repr(outcome1))
    print("turn one types=" + repr(types1))
    print("turn one api_retry=" + repr(retry1))
    if outcome1 in ("timeout", "eof"):
        print("turn one could not complete")
        cleanup()
        return

    print("--- turn two ---")
    send(_user_turn("Reply with exactly the letter B and nothing else."))
    outcome2, types2, retry2 = read_until_result(180)
    print("turn two outcome=" + repr(outcome2))
    print("turn two types=" + repr(types2))
    print("turn two api_retry=" + repr(retry2))
    if outcome2 not in ("timeout", "eof"):
        print("PASS: turn two produced a result; no second-message hang on this host")
    else:
        print("FAIL: turn two did not complete; reproduces the known Windows second message hang")

    cleanup()


if __name__ == "__main__":
    main()
