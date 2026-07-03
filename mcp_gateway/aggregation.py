"""Tushare 工具聚合:把上游 tool-per-API 的 258 个工具在网关层收成 ~13 个分类分发工具。

机制(已 spike 验证):
- ``on_list_tools``:把 ``{raw_prefix}*`` 的原始工具从列表抹掉,替换成 ``{cat_prefix}{bucket}``
  合成分类工具(``api_name`` enum + ``params`` 透传)。被隐藏的原始工具仍是 mounted、仍可被调用。
- ``on_call_tool``:把分类工具调用改写回 ``{raw_prefix}{api_name}``,经 ``call_next`` 走原有
  proxy 路由到上游。per-API 参数 schema 的损失是门面聚合的固有代价(与 REST 侧
  ``/tdx/call/{method}`` 同一权衡)。

归组运行时从工具 description 头部的官方分类路径 ``/数据接口/<L1>/<L2>/<L3>-说明`` 解析,
Tushare 以后新增接口自动落入对应桶;解析不出的落 ``misc`` 兜底桶,绝不丢工具。
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware
from fastmcp.tools import Tool

# ---- 归一化映射:原始 L1(近重复较多)→ 干净桶 -----------------------------
# 沪深股票一家独占 120 个 API,按 L2 再拆三桶;其余按 L1 合并近重复命名空间。
_STOCK_L1 = "沪深股票"
_STOCK_L2_QUOTE = {"行情数据", "打板专题数据", "资金流向数据"}
_STOCK_L2_FIN = {"财务数据"}

_L1_BUCKET: dict[str, str] = {
    "指数": "index", "指数专题": "index",
    "公募基金": "fund", "ETF专题": "fund", "财富管理": "fund",
    "债券": "bond", "债券专题": "bond",
    "期货": "futures", "期货数据": "futures",
    "期权": "option", "期权数据": "option",
    "港股": "hk", "港股数据": "hk",
    "美股": "us", "美股数据": "us",
    "外汇": "fx_spot", "外汇数据": "fx_spot", "现货": "fx_spot", "现货数据": "fx_spot",
    "宏观经济": "macro",
    "行业经济": "alt", "另类数据": "alt", "大模型语料专题数据": "alt", "小佩数据": "alt",
}

MISC_BUCKET = "misc"

# 展示顺序 + 中文标签(进合成工具的 description)。
BUCKET_LABELS: dict[str, str] = {
    "stock_quote": "沪深股票·行情/打板/资金流",
    "stock_fin": "沪深股票·财务数据",
    "stock_ref": "沪深股票·基础/参考/特色/两融",
    "index": "指数",
    "fund": "公募基金/ETF",
    "bond": "债券/可转债",
    "futures": "期货",
    "option": "期权",
    "hk": "港股",
    "us": "美股",
    "fx_spot": "外汇/黄金现货",
    "macro": "宏观经济",
    "alt": "行业经济/新闻/另类数据",
    MISC_BUCKET: "其他(自选股组合等)",
}


@dataclass(frozen=True)
class ApiEntry:
    """一个被聚合的原始 API(去前缀名 + 官方中文名 + 必填参数)。"""

    api: str
    label: str  # 分类路径最末级中文名,如 "日线行情";解析不出为空串
    required: tuple[str, ...] = ()  # 上游 schema 的必填参数,进 description 提示


def classify(description: str | None) -> tuple[str, str]:
    """从工具 description 解析 (bucket, 末级中文名)。

    description 形如 ``/数据接口/<L1>/<L2>/<L3>-说明``;编码坏/格式变/缺失 → misc。
    """
    head = (description or "").strip().split("-", 1)[0]
    parts = [p for p in head.split("/") if p]
    if parts and parts[0] == "数据接口":
        parts = parts[1:]
    if not parts:
        return MISC_BUCKET, ""
    l1 = parts[0]
    label = parts[-1] if len(parts) > 1 else ""
    if l1 == _STOCK_L1:
        l2 = parts[1] if len(parts) > 1 else ""
        if l2 in _STOCK_L2_QUOTE:
            return "stock_quote", label
        if l2 in _STOCK_L2_FIN:
            return "stock_fin", label
        return "stock_ref", label
    return _L1_BUCKET.get(l1, MISC_BUCKET), label


def group_tools(tools, raw_prefix: str) -> dict[str, list[ApiEntry]]:
    """把 ``{raw_prefix}*`` 工具按 classify 归桶;返回 bucket → [ApiEntry](按 api 排序)。"""
    groups: dict[str, list[ApiEntry]] = defaultdict(list)
    for t in tools:
        if not t.name.startswith(raw_prefix):
            continue
        bucket, label = classify(t.description)
        schema = getattr(t, "parameters", None) or {}
        groups[bucket].append(ApiEntry(
            api=t.name.removeprefix(raw_prefix),
            label=label,
            required=tuple(schema.get("required") or ()),
        ))
    return {b: sorted(entries, key=lambda e: e.api) for b, entries in groups.items()}


def build_category_tool(cat_prefix: str, bucket: str, entries: list[ApiEntry]) -> Tool:
    """构造一个合成分类工具(api_name enum + params 透传)。"""

    def member(e: ApiEntry) -> str:
        req = f";必填:{','.join(e.required)}" if e.required else ""
        return f"{e.api}({e.label}{req})" if (e.label or req) else e.api

    members = ", ".join(member(e) for e in entries)
    label = BUCKET_LABELS.get(bucket, bucket)
    return Tool(
        name=f"{cat_prefix}{bucket}",
        description=(
            f"Tushare {label} 分类分发工具。用 api_name 选择数据接口,"
            f"params 传该接口原生参数(如 ts_code/trade_date/start_date/end_date,"
            f"日期格式 YYYYMMDD;fields 须为字符串数组而非逗号串)。可选 api_name: {members}"
        ),
        parameters={
            "type": "object",
            "properties": {
                "api_name": {
                    "type": "string",
                    "enum": [e.api for e in entries],
                    "description": "要调用的 Tushare 数据接口名",
                },
                "params": {
                    "type": "object",
                    "description": "该接口的原生参数,原样透传上游",
                },
            },
            "required": ["api_name"],
        },
    )


def _split_csv(v: str) -> list[str]:
    return [s.strip() for s in v.split(",") if s.strip()]


def _coerce_params(params: dict, schema: dict | None = None) -> dict:
    """按上游真实 schema 纠偏参数形态(聚合吞掉 per-API schema 后模型易猜错)。不改原 dict。

    全量 schema 普查(258 工具)发现的坑,全部在此收口:
    - array 参数(fields 258 处):模型按 Tushare 原生 REST 习惯传逗号串 → 拆数组
    - string 参数(980 处,如 limit/offset 多数是 string):模型传数字 → str()
    - integer/number 参数(6 处,且与 string 同名混用):模型传数字串 → int()/float()
    schema 未知(list 前直调)时保底只处理 fields 逗号串。
    """
    props = (schema or {}).get("properties", {})
    out = dict(params)
    for k, v in params.items():
        expect = props.get(k, {}).get("type")
        if expect is None:
            if k == "fields" and isinstance(v, str) and v.strip():
                out[k] = _split_csv(v)
            continue
        if expect == "array" and isinstance(v, str) and v.strip():
            out[k] = _split_csv(v)
        elif expect == "string" and isinstance(v, (int, float)) and not isinstance(v, bool):
            out[k] = str(v)
        elif expect == "integer" and isinstance(v, str) and v.strip().lstrip("-").isdigit():
            out[k] = int(v)
        elif expect == "number" and isinstance(v, str):
            try:
                out[k] = float(v)
            except ValueError:
                pass  # 转不了就原样透传,让上游报语义错误
    return out


class ToolAggregationMiddleware(Middleware):
    """网关层门面聚合中间件(仅处理 raw_prefix 命名空间,其余厂商零影响)。"""

    def __init__(self, raw_prefix: str, cat_prefix: str) -> None:
        self.raw_prefix = raw_prefix
        self.cat_prefix = cat_prefix
        # bucket → api 集合,list_tools 时刷新;调用时用于成员校验(未刷新前放行改写)。
        self._api_index: dict[str, set[str]] = {}
        # api → 上游真实 inputSchema,list_tools 时缓存;调用时做参数纠偏 + 必填快速校验。
        self._schemas: dict[str, dict] = {}

    async def on_list_tools(self, context, call_next):
        tools = await call_next(context)
        kept = [t for t in tools if not t.name.startswith(self.raw_prefix)]
        groups = group_tools(tools, self.raw_prefix)
        if not groups:
            return kept
        self._api_index = {b: {e.api for e in entries} for b, entries in groups.items()}
        self._schemas = {
            t.name.removeprefix(self.raw_prefix): getattr(t, "parameters", None) or {}
            for t in tools
            if t.name.startswith(self.raw_prefix)
        }
        order = list(BUCKET_LABELS)
        synth = [
            build_category_tool(self.cat_prefix, bucket, groups[bucket])
            for bucket in sorted(groups, key=lambda b: order.index(b) if b in order else 99)
        ]
        return kept + synth

    async def on_call_tool(self, context, call_next):
        name = context.message.name
        if not name.startswith(self.cat_prefix):
            return await call_next(context)
        bucket = name.removeprefix(self.cat_prefix)
        args = context.message.arguments or {}
        api = args.get("api_name")
        if not api or not isinstance(api, str):
            raise ToolError(f"{name} 需要 api_name 参数(见工具 description 的可选值)")
        known = self._api_index.get(bucket)
        if known is not None and api not in known:
            raise ToolError(f"api_name={api!r} 不属于 {name},先 tools/list 查看可选值")
        schema = self._schemas.get(api)
        coerced = _coerce_params(args.get("params") or {}, schema)
        if schema:
            missing = [r for r in schema.get("required", ()) if coerced.get(r) in (None, "")]
            if missing:
                raise ToolError(f"{api} 缺必填参数: {','.join(missing)}(在 params 里传)")
        new_msg = context.message.model_copy(
            update={"name": f"{self.raw_prefix}{api}", "arguments": coerced}
        )
        return await call_next(context.copy(message=new_msg))
