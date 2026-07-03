"""Tushare 工具聚合(网关层门面)单测:归组引擎 + 中间件隐藏/改写 + 非聚合厂商零影响。

全 in-memory(桩上游),不触发真实登录/网络。
"""
import pytest
from fastmcp import Client, FastMCP
from fastmcp.server import create_proxy

from mcp_gateway.aggregation import (
    MISC_BUCKET,
    ToolAggregationMiddleware,
    build_category_tool,
    classify,
    group_tools,
)
from mcp_gateway.providers import TUSHARE

# 异步用例走 anyio 插件(仅 asyncio 后端,.venv-mcp 未装 trio)
pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


# ---- 归组引擎(纯函数,静态样本钉住真实 description 格式) --------------------

class TestClassify:
    def test_stock_quote_bucket(self):
        # 真实样本:daily 的 description 头部
        bucket, label = classify("/数据接口/沪深股票/行情数据/日线行情-获取股票行情数据")
        assert bucket == "stock_quote"
        assert label == "日线行情"

    def test_stock_moneyflow_goes_quote(self):
        bucket, _ = classify("/数据接口/沪深股票/资金流向数据/个股资金流向-...")
        assert bucket == "stock_quote"

    def test_stock_fin_bucket(self):
        bucket, _ = classify("/数据接口/沪深股票/财务数据/利润表-获取上市公司财务利润表数据")
        assert bucket == "stock_fin"

    def test_stock_other_l2_goes_ref(self):
        bucket, _ = classify("/数据接口/沪深股票/基础数据/股票列表-获取基础信息数据")
        assert bucket == "stock_ref"

    def test_near_duplicate_l1_merged(self):
        # 指数 与 指数专题 归同一桶;期货/期货数据 同理
        b1, _ = classify("/数据接口/指数/指数基本信息-...")
        b2, _ = classify("/数据接口/指数专题/指数日线行情-...")
        assert b1 == b2 == "index"
        f1, _ = classify("/数据接口/期货/日线行情-...")
        f2, _ = classify("/数据接口/期货数据/合约信息-...")
        assert f1 == f2 == "futures"

    def test_unknown_l1_falls_to_misc(self):
        bucket, _ = classify("/数据接口/股票数据/自选股组合/自选股管理-...")
        assert bucket == MISC_BUCKET

    def test_garbage_and_empty_fall_to_misc(self):
        assert classify(None)[0] == MISC_BUCKET
        assert classify("")[0] == MISC_BUCKET
        assert classify("no slash path at all")[0] == MISC_BUCKET


class _T:
    """轻量桩:只带 name/description 的工具对象。"""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description


class TestGroupTools:
    def test_groups_only_prefixed_tools(self):
        tools = [
            _T("tushare_ds_daily", "/数据接口/沪深股票/行情数据/日线行情-x"),
            _T("tushare_ds_income", "/数据接口/沪深股票/财务数据/利润表-x"),
            _T("ifind_stock_get_stock_summary", "别家的,不许动"),
        ]
        groups = group_tools(tools, "tushare_ds_")
        assert set(groups) == {"stock_quote", "stock_fin"}
        assert groups["stock_quote"][0].api == "daily"
        assert groups["stock_quote"][0].label == "日线行情"

    def test_category_tool_schema(self):
        groups = group_tools(
            [_T("tushare_ds_daily", "/数据接口/沪深股票/行情数据/日线行情-x")],
            "tushare_ds_",
        )
        tool = build_category_tool("tushare_cat_", "stock_quote", groups["stock_quote"])
        assert tool.name == "tushare_cat_stock_quote"
        assert tool.parameters["properties"]["api_name"]["enum"] == ["daily"]
        assert "daily(日线行情)" in tool.description
        assert tool.parameters["required"] == ["api_name"]


# ---- 中间件端到端(in-memory 网关 + 桩上游) ---------------------------------

@pytest.fixture
def gateway():
    child = FastMCP(name="stub-tushare")

    @child.tool(description="/数据接口/沪深股票/行情数据/日线行情-获取股票行情")
    def daily(ts_code: str = "") -> str:
        return f"daily-{ts_code}"

    @child.tool(description="/数据接口/沪深股票/财务数据/利润表-获取利润表")
    def income(ts_code: str = "") -> str:
        return f"income-{ts_code}"

    @child.tool(description="/数据接口/沪深股票/行情数据/分钟行情-获取分钟行情")
    def stk_mins(ts_code: str, freq: str) -> str:
        return f"mins-{ts_code}-{freq}"

    other = FastMCP(name="stub-ifind")

    @other.tool(description="别家工具")
    def get_stock_summary(query: str = "") -> str:
        return f"summary-{query}"

    gw = FastMCP(name="gw")
    gw.mount(create_proxy(child), namespace="tushare_ds")
    gw.mount(create_proxy(other), namespace="ifind_stock")
    gw.add_middleware(ToolAggregationMiddleware("tushare_ds_", "tushare_cat_"))
    return gw


class TestMiddleware:
    async def test_list_hides_raw_and_adds_categories(self, gateway):
        async with Client(gateway) as c:
            names = {t.name for t in await c.list_tools()}
        assert not any(n.startswith("tushare_ds_") for n in names)
        assert {"tushare_cat_stock_quote", "tushare_cat_stock_fin"} <= names

    async def test_non_aggregated_provider_untouched(self, gateway):
        async with Client(gateway) as c:
            names = {t.name for t in await c.list_tools()}
        assert "ifind_stock_get_stock_summary" in names

    async def test_call_rewrites_to_hidden_tool(self, gateway):
        async with Client(gateway) as c:
            r = await c.call_tool(
                "tushare_cat_stock_quote",
                {"api_name": "daily", "params": {"ts_code": "600519.SH"}},
            )
        assert "daily-600519.SH" in r.content[0].text

    async def test_call_without_params_defaults_empty(self, gateway):
        async with Client(gateway) as c:
            r = await c.call_tool("tushare_cat_stock_quote", {"api_name": "daily"})
        assert "daily-" in r.content[0].text

    async def test_missing_api_name_rejected(self, gateway):
        async with Client(gateway) as c:
            with pytest.raises(Exception, match="api_name"):
                await c.call_tool("tushare_cat_stock_quote", {"params": {}})

    async def test_wrong_bucket_api_rejected_after_list(self, gateway):
        async with Client(gateway) as c:
            await c.list_tools()  # 刷新成员索引
            with pytest.raises(Exception, match="income"):
                # income 属于 stock_fin,不能经 stock_quote 调
                await c.call_tool("tushare_cat_stock_quote", {"api_name": "income"})

    async def test_direct_call_of_other_provider_passes(self, gateway):
        async with Client(gateway) as c:
            r = await c.call_tool("ifind_stock_get_stock_summary", {"query": "q"})
        assert "summary-q" in r.content[0].text

    async def test_missing_required_fast_fails_locally(self, gateway):
        # stk_mins 必填 ts_code+freq;list 后缓存 schema,漏传应本地快速报错(不打上游)
        async with Client(gateway) as c:
            await c.list_tools()
            with pytest.raises(Exception, match="必填"):
                await c.call_tool("tushare_cat_stock_quote",
                                  {"api_name": "stk_mins", "params": {"freq": "1min"}})

    async def test_int_coerced_to_string_by_schema(self, gateway):
        # daily 的 ts_code 是 string,模型传 int 应被纠偏后成功
        async with Client(gateway) as c:
            await c.list_tools()
            r = await c.call_tool("tushare_cat_stock_quote",
                                  {"api_name": "daily", "params": {"ts_code": 600519}})
        assert "daily-600519" in r.content[0].text

    async def test_required_hint_in_description(self, gateway):
        async with Client(gateway) as c:
            tools = {t.name: t for t in await c.list_tools()}
        desc = tools["tushare_cat_stock_quote"].description
        assert "stk_mins(分钟行情;必填:ts_code,freq)" in desc


class TestCoerceParams:
    """按上游 schema 纠偏参数形态(聚合吞掉 per-API schema 后模型按 REST 文档传参的坑)。"""

    def test_comma_string_split_without_schema(self):
        # schema 未知时保底:仅 fields 逗号串拆数组
        from mcp_gateway.aggregation import _coerce_params

        out = _coerce_params({"ts_code": "600519.SH", "fields": "ts_code, close ,open"})
        assert out["fields"] == ["ts_code", "close", "open"]
        assert out["ts_code"] == "600519.SH"

    def test_schema_aware_coercions(self):
        from mcp_gateway.aggregation import _coerce_params

        schema = {"properties": {
            "fields": {"type": "array"},
            "limit": {"type": "integer"},
            "curve_term": {"type": "number"},
            "trade_date": {"type": "string"},
        }}
        out = _coerce_params(
            {"fields": "a,b", "limit": "10", "curve_term": "0.5", "trade_date": 20260701},
            schema,
        )
        assert out == {"fields": ["a", "b"], "limit": 10, "curve_term": 0.5,
                       "trade_date": "20260701"}

    def test_unconvertible_passthrough_and_bool_untouched(self):
        from mcp_gateway.aggregation import _coerce_params

        schema = {"properties": {"n": {"type": "number"}, "s": {"type": "string"}}}
        out = _coerce_params({"n": "abc", "s": True}, schema)
        assert out == {"n": "abc", "s": True}  # 转不了原样透传;bool 不当数字转

    def test_array_untouched_and_original_not_mutated(self):
        from mcp_gateway.aggregation import _coerce_params

        src = {"fields": ["a", "b"]}
        assert _coerce_params(src)["fields"] == ["a", "b"]
        src2 = {"fields": "a,b"}
        _coerce_params(src2)
        assert src2["fields"] == "a,b"  # 不可变:原 dict 不被改

    def test_empty_and_absent_passthrough(self):
        from mcp_gateway.aggregation import _coerce_params

        assert _coerce_params({}) == {}
        assert _coerce_params({"fields": ""}) == {"fields": ""}


class TestProviderFlag:
    def test_tushare_aggregate_enabled(self):
        assert TUSHARE.aggregate is True

    def test_others_default_off(self):
        from mcp_gateway.providers import IFIND, MX

        assert IFIND.aggregate is False
        assert MX.aggregate is False
