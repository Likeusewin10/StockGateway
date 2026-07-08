import json, sys, io, os, re

SRC = r"C:\Users\wyfei\.claude\projects\D--dev-Project-StockSDK\fc957d55-dad2-4e40-954a-5ba63e1ec54f.jsonl"
OUT = r"D:\dev\Project\StockSDK\docs\会话记录-多机AgentMCP协同.md"
START_LINE = 12  # /ecc:plan 多机协同 起点（0-indexed 行号）

# ---- 脱敏：组织红线「Never Include PII」+ 项目「凭据不入库/不打印」优先于「原封不动」----
# 收集本机磁盘上的真实凭据字面量 + 通用凭据形状正则，导出前一律打码。
_ROOT = r"D:\dev\Project\StockSDK"
_literal_secrets = set()
for fn in (".env", "frpc.secret.bat", "frpc.secret.sh"):
    p = os.path.join(_ROOT, fn)
    if os.path.exists(p):
        for ln in io.open(p, encoding="utf-8", errors="ignore"):
            ln = ln.strip()
            for sep in ("=", ":"):
                if sep in ln:
                    v = ln.split(sep, 1)[1].strip().strip('"').strip("'")
                    # 只收像凭据的长随机串，避免误伤普通配置
                    if len(v) >= 16 and re.fullmatch(r"[A-Za-z0-9_\-\.]+", v):
                        _literal_secrets.add(v)

_secret_patterns = [
    re.compile(r'((?:API_KEY|PEER_[A-Z0-9_]*API_KEY|FRP_TOKEN|IFIND_MCP_JWT|TUSHARE_MCP_TOKEN|MIAO_XIANG_MCP_KEY)\s*[=:]\s*)([A-Za-z0-9_\-\.]{12,})'),
    re.compile(r'((?:X-API-Key|Authorization)\s*[:=]\s*)(Bearer\s+)?([A-Za-z0-9_\-\.]{12,})', re.I),
    re.compile(r'([?&]token=)([A-Za-z0-9_\-\.]{12,})'),
    re.compile(r'("(?:api_key|token|password|secret|X-API-Key|x-api-key)"\s*:\s*")([^"]{12,})(")'),
]

def redact(s: str) -> str:
    if not s:
        return s
    for lit in _literal_secrets:
        s = s.replace(lit, "<REDACTED>")
    s = _secret_patterns[0].sub(lambda m: m.group(1) + "<REDACTED>", s)
    s = _secret_patterns[1].sub(lambda m: m.group(1) + (m.group(2) or "") + "<REDACTED>", s)
    s = _secret_patterns[2].sub(lambda m: m.group(1) + "<REDACTED>", s)
    s = _secret_patterns[3].sub(lambda m: m.group(1) + "<REDACTED>" + m.group(3), s)
    return s


def get_text_blocks(content):
    """返回 [(kind, payload)]，kind ∈ text/thinking/tool_use/tool_result。"""
    out = []
    if isinstance(content, str):
        if content.strip():
            out.append(("text", content))
        return out
    if not isinstance(content, list):
        return out
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "text":
            if b.get("text", "").strip():
                out.append(("text", b["text"]))
        elif t == "thinking":
            out.append(("thinking", b.get("thinking", "")))
        elif t == "tool_use":
            out.append(("tool_use", b))
        elif t == "tool_result":
            out.append(("tool_result", b))
    return out

def render_tool_result_content(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for b in c:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(b.get("text", ""))
                else:
                    parts.append(json.dumps(b, ensure_ascii=False))
            else:
                parts.append(str(b))
        return "\n".join(parts)
    return json.dumps(c, ensure_ascii=False)

lines = io.open(SRC, encoding="utf-8").read().splitlines()
md = []
md.append("# 会话记录：MCP 多机 Agent 协同（hub 星形聚合）\n")
md.append("> 本文由会话原始 JSONL（`fc957d55-…jsonl`）逐条 verbatim 导出，起自 `/ecc:plan 多机协同`。\n")
md.append("> - 用户发言、助手回复正文、每次工具调用及其返回结果均为**原文照录**（超长工具结果按标注截断）。\n")
md.append("> - 🔴 **思考链路无法还原**：Claude Code 不把扩展思考的明文写入会话日志，JSONL 中 thinking 块正文为空、仅存加密签名。下文相应位置以占位标注，未做任何补写/杜撰。\n")
md.append("> - 已省略 harness 注入的 attachment / mode / system-reminder / file-history 等非对话管道记录。\n")
md.append("\n---\n")

turn_no = 0
CAP = 16000  # 单个工具结果超过此长度则截断（保留原文可读性）

for idx in range(START_LINE, len(lines)):
    line = lines[idx].strip()
    if not line:
        continue
    try:
        o = json.loads(line)
    except Exception:
        continue
    typ = o.get("type")
    if typ not in ("user", "assistant"):
        continue
    msg = o.get("message") or {}
    role = msg.get("role")
    content = msg.get("content")
    blocks = get_text_blocks(content)
    if not blocks:
        continue

    # 判定是否人类真实发言（区别于 tool_result 回灌到 user 角色）
    only_tool_result = all(k == "tool_result" for k, _ in blocks)

    for kind, payload in blocks:
        if kind == "text":
            if role == "user":
                turn_no += 1
                md.append(f"\n## 👤 用户\n")
                md.append(payload.rstrip() + "\n")
            else:
                md.append(f"\n### 🤖 助手\n")
                md.append(payload.rstrip() + "\n")
        elif kind == "thinking":
            md.append("\n> 💭 *[思考内容未存于会话日志——仅加密签名，无法 verbatim 还原]*\n")
        elif kind == "tool_use":
            name = payload.get("name", "?")
            inp = payload.get("input", {})
            inp_str = json.dumps(inp, ensure_ascii=False, indent=2)
            if len(inp_str) > CAP:
                inp_str = inp_str[:CAP] + f"\n… [截断，原长 {len(inp_str)} 字符]"
            md.append(f"\n<details>\n<summary>🔧 工具调用: <code>{name}</code></summary>\n\n```json\n{inp_str}\n```\n</details>\n")
        elif kind == "tool_result":
            txt = render_tool_result_content(payload.get("content"))
            is_err = payload.get("is_error")
            if len(txt) > CAP:
                txt = txt[:CAP] + f"\n… [截断，原长 {len(txt)} 字符]"
            tag = "❌ 工具结果(错误)" if is_err else "📤 工具结果"
            md.append(f"\n<details>\n<summary>{tag}</summary>\n\n```\n{txt}\n```\n</details>\n")

io.open(OUT, "w", encoding="utf-8", newline="").write(redact("\n".join(md)))
print("written:", OUT)
print("size KB:", round(os.path.getsize(OUT)/1024, 1))
print("human turns approx:", turn_no)
print("literal secrets scrubbed:", len(_literal_secrets))
# 二次校验：导出文件不得残留已知凭据字面量
final = io.open(OUT, encoding="utf-8").read()
leak = [lit for lit in _literal_secrets if lit in final]
print("LEAK CHECK:", "PASS (无残留)" if not leak else f"FAIL 残留 {len(leak)} 个")
