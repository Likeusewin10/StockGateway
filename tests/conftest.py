"""测试夹具：在导入任何 stocksdk 路由前，把 SDK 替换为可控的假模块。

EmQuantAPI / iFinDPy 依赖 Windows DLL 与真实登录，测试中一律不加载真品。
这里在 sys.modules 注入桩，使路由与会话逻辑可在纯 Python 下测试。
"""
import sys
import types

import pytest


class FakeEmResult:
    """模拟 EM SDK 返回对象：带 ErrorCode/ErrorMsg/Data。"""

    def __init__(self, error_code=0, error_msg="", data=None, serial_id=None):
        self.ErrorCode = error_code
        self.ErrorMsg = error_msg
        self.Data = data if data is not None else {}
        if serial_id is not None:
            self.SerialID = serial_id


class FakeEmClient:
    """模拟 EmQuantAPI.c。测试通过设置属性控制返回。"""

    def __init__(self):
        self._csd_result = FakeEmResult(data={"x": 1})
        self._css_result = FakeEmResult(data={"x": 2})

    def start(self, *a, **k):
        return FakeEmResult(error_code=0)

    def stop(self, *a, **k):
        return FakeEmResult(error_code=0)

    def csd(self, *a, **k):
        return self._csd_result

    def css(self, *a, **k):
        return self._css_result

    def edb(self, *a, **k):
        return FakeEmResult(data={"edb": 1})

    def csq(self, *a, **k):
        return FakeEmResult(serial_id=42)

    def csqcancel(self, *a, **k):
        return FakeEmResult()

    def porder(self, *a, **k):
        # 组合下单（虚拟组合持仓加减，无真实资金）；桩返回成功
        return FakeEmResult(data={"order": "ok"})

    def pquery(self, *a, **k):
        return FakeEmResult(data={"combins": []})


class FakeWindData:
    """模拟 WindPy WindData 对象：带 ErrorCode/Codes/Fields/Times/Data。"""

    def __init__(self, error_code=0, codes=None, fields=None, times=None, data=None):
        self.ErrorCode = error_code
        self.Codes = codes if codes is not None else []
        self.Fields = fields if fields is not None else []
        self.Times = times if times is not None else []
        self.Data = data if data is not None else []


class FakeWindClient:
    """模拟 WindPy.w。usedf=True 时返回 (ErrorCode, DataFrame) 元组，否则返回 WindData。"""

    def start(self, *a, **k):
        return FakeWindData(error_code=0, data=["OK!"])

    def stop(self, *a, **k):
        return None

    def isconnected(self, *a, **k):
        return True

    def _emit(self, usedf, codes, fields):
        if usedf:
            import pandas as pd
            df = pd.DataFrame({f: [1.0] for f in fields}, index=["2024-01-05"])
            return 0, df
        return FakeWindData(error_code=0, codes=codes, fields=fields,
                            times=["2024-01-05"], data=[[1.0] for _ in fields])

    def wsd(self, codes, fields, *a, usedf=False, **k):
        return self._emit(usedf, [codes], [fields])

    def wss(self, codes, fields, *a, usedf=False, **k):
        return self._emit(usedf, [codes], [fields])

    def wset(self, *a, usedf=False, **k):
        return self._emit(usedf, ["x"], ["f"])

    def edb(self, *a, usedf=False, **k):
        return self._emit(usedf, ["M0017126"], ["edb"])

    def tdays(self, *a):
        # 日期函数不接受 usedf 关键字：用于测试透传的 TypeError 退回路径
        return FakeWindData(error_code=0, data=[["2024-01-05"]])

    def wsq(self, *a, **k):
        # 实时行情(异步回调);桩同步返回,仅供 methods 标注/透传存在性
        return FakeWindData(error_code=0)

    def torder(self, *a, **k):
        # 交易函数：不应被透传调用到（路由层 403 拦截）；桩存在仅供 methods 标注
        return FakeWindData(error_code=0)


# ----------------------------- 通达信 TQ 桩 -----------------------------

class FakeTdxClient:
    """模拟 tqcenter.tq（类，方法直接调用）。返回结构对齐官方文档。

    测试钩子：
    - get_market_data 对 code=='FAIL.SH' 返回空 dict（取数失败模拟）
    - 各 dict 返回带 'ErrorId':'0'；snapshot/stock_info 为扁平 dict
    """

    def initialize(self, *a, **k):
        return None

    def close(self, *a, **k):
        return None

    def get_market_data(self, field_list=None, stock_list=None, period="1d", start_time="",
                        end_time="", count=-1, dividend_type="none", fill_data=True):
        import pandas as pd
        codes = stock_list or ["600519.SH"]
        idx = codes
        return {
            "Close": pd.DataFrame({"2026-06-30": [1185.49] * len(idx)}, index=idx),
            "Open": pd.DataFrame({"2026-06-30": [1187.0] * len(idx)}, index=idx),
            "ForwardFactor": pd.DataFrame({"2026-06-30": [1.0] * len(idx)}, index=idx),
        }

    def get_market_snapshot(self, stock_code, field_list=None):
        return {"ItemNum": "3342", "LastClose": "34.21", "Now": "35.06",
                "Buyp": ["35.05", "35.04"], "Sellp": ["35.06", "35.07"], "ErrorId": "0"}

    def get_stock_info(self, stock_code, field_list=None):
        return {"Name": "贵州茅台", "Unit": "100", "BelongHS300": "1", "ErrorId": "0"}

    def get_financial_data(self, stock_list=None, field_list=None, start_time="",
                          end_time="", report_type="report_time"):
        return {"Fn193": {"688318.SH": 1.23}, "ErrorId": "0"}

    def get_stock_list_in_sector(self, block_code, block_type=0, list_type=0):
        return [{"Code": "600456.SH", "Name": "宝钛股份"}] if list_type else ["600456.SH"]

    def get_stock_list(self, market=None, list_type=0):
        return [{"Code": "600000.SH", "Name": "浦发银行"}] if list_type else ["600000.SH"]

    def get_trading_dates(self, market, start_time="", end_time="", count=-1):
        return ["20260629", "20260630"]

    def get_divid_factors(self, stock_code, start_time="", end_time=""):
        import pandas as pd
        return pd.DataFrame({"factor": [1.0]}, index=["2026-06-30"])

    def order_stock(self, account_id=-1, stock_code="", order_type=0, order_volume=0,
                    price_type=0, price=0.0, notify=0):
        # 交易函数：正常返回 {'ErrorId','Msg','Value'}，Value 1=待确认。FAIL.SH → Value 0 失败。
        if stock_code == "FAIL.SH":
            return {"ErrorId": "0", "Msg": "资金不足", "Value": 0}
        return {"ErrorId": "0", "Msg": "已发送信号至客户端，待用户确认！", "Value": 1, "Wtbh": "58545"}

    def cancel_order_stock(self, account_id=-1, stock_code="", order_id=""):
        # order_id==-999 → Value 0 撤单失败；否则 Value 1 成功。
        if order_id == -999:
            return {"ErrorId": "0", "Msg": "委托已完成", "Value": 0}
        return {"ErrorId": "0", "Msg": "撤单已受理", "Value": 1}

    def stock_account(self, account="", account_type="STOCK"):
        return 0   # int 句柄（合法值可为 0）

    def query_stock_asset(self, account_id=-1):
        return {"Currency": "人民币", "Balance": "30234.070", "Cash": "30234.070",
                "Asset": "1233041.070", "MarketValue": "1201690.000", "ErrorId": "0"}

    def query_stock_positions(self, account_id=-1):
        return [{"Code": "000001.SZ", "Cbj": "10.693", "TotalVol": "100", "CanUseVol": "100"}]

    def query_stock_orders(self, account_id=-1, stock_code="", cancelable_only=False):
        return [{"Wtbh": "58545", "Code": "688318.SH", "Time": "93853", "BSFlag": -1,
                 "Status": 0, "WtPrice": "125.000", "WtVol": "1000"}]

    def subscribe_hq(self, *a, **k):
        return {"ErrorId": "0"}

    def send_message(self, *a, **k):
        return {"ErrorId": "0"}


# ----------------------------- QMT（XtQuant）桩 -----------------------------
class _Obj:
    """通用属性容器，模拟 xttype 的 Xt* 数据对象。"""

    def __init__(self, **kw):
        self.__dict__.update(kw)


class FakeStockAccount:
    def __init__(self, account_id, account_type="STOCK"):
        self.account_id = account_id
        self.account_type = account_type


class FakeXtQuantTraderCallback:
    """基类桩：真实库里是带 on_* 钩子的回调基类。"""
    pass


class FakeXtQuantTrader:
    """模拟 XtQuantTrader。测试钩子：

    - order_stock 对 stock_code=='FAIL.SH' 返回 -1（下单失败）
    - cancel_order_stock 对 order_id==-999 返回 -3（未登录），否则 0
    - connect 返回 0（已就绪）
    """

    def __init__(self, path, session_id):
        self.path = path
        self.session_id = session_id
        self._cb = None

    def register_callback(self, cb):
        self._cb = cb

    def start(self):
        return None

    def connect(self):
        return 0

    def subscribe(self, account):
        return 0

    def order_stock(self, account, stock_code, order_type, volume, price_type, price,
                    strategy="", remark=""):
        return -1 if stock_code == "FAIL.SH" else 12345

    def cancel_order_stock(self, account, order_id):
        return -3 if order_id == -999 else 0

    def query_stock_asset(self, account):
        return _Obj(account_id=getattr(account, "account_id", None), cash=100000.0,
                    frozen_cash=0.0, market_value=50000.0, total_asset=150000.0)

    def query_stock_positions(self, account):
        return [_Obj(account_id=getattr(account, "account_id", None), stock_code="600000.SH",
                     volume=1000, can_use_volume=1000, open_price=10.0, market_value=10500.0,
                     frozen_volume=0, on_road_volume=0, yesterday_volume=1000)]

    def query_stock_orders(self, account, cancelable_only=False):
        return [_Obj(account_id=getattr(account, "account_id", None), stock_code="600000.SH",
                     order_id=12345, order_sysid="S1", order_time=0, order_type=23,
                     order_volume=1000, price_type=11, price=10.5, traded_volume=0,
                     traded_price=0.0, order_status=50, status_msg="已报",
                     strategy_name="sts", order_remark="")]

    def query_stock_trades(self, account):
        return [_Obj(account_id=getattr(account, "account_id", None), stock_code="600000.SH",
                     order_type=23, traded_id="T1", traded_time=0, traded_price=10.5,
                     traded_volume=1000, traded_amount=10500.0, order_id=12345, order_sysid="S1",
                     strategy_name="sts", order_remark="")]


class FakeXtData:
    """模拟 xtdata 行情模块。"""

    def get_market_data_ex(self, field_list, stock_list, period="1d", start_time="",
                           end_time="", count=-1, dividend_type="none", fill_data=True):
        import pandas as pd
        codes = stock_list or ["600000.SH"]
        return {"close": pd.DataFrame({"20240105": [10.5] * len(codes)}, index=codes)}

    def get_full_tick(self, code_list):
        code = code_list[0] if code_list else "600000.SH"
        return {code: {"lastPrice": 10.5, "volume": 1000, "askPrice1": 10.51}}

    def get_stock_list_in_sector(self, sector_name):
        return ["600000.SH", "000001.SZ"]

    def get_trading_dates(self, market, start_time="", end_time="", count=-1):
        return [1704412800000]

    def get_instrument_detail(self, stock_code, iscomplete=False):
        return {"InstrumentID": stock_code, "InstrumentName": "测试股"}

    def download_history_data(self, stock_code, period, start_time="", end_time=""):
        return None

    def subscribe_quote(self, *a, **k):
        return 0


def _install_fake_sdks():
    # EmQuantAPI 模块，导出 c
    em_mod = types.ModuleType("EmQuantAPI")
    em_mod.c = FakeEmClient()
    sys.modules["EmQuantAPI"] = em_mod

    # iFinDPy 模块，导出所有用到的 THS_ 函数
    ths_mod = types.ModuleType("iFinDPy")

    def _ok_dict(*a, **k):
        return {"errorcode": 0, "tables": []}

    ths_mod.THS_iFinDLogin = lambda user, pwd: 0
    ths_mod.THS_iFinDLogout = lambda *a, **k: 0
    ths_mod.THS_HistoryQuotes = _ok_dict
    ths_mod.THS_BasicData = _ok_dict
    ths_mod.THS_RealtimeQuotes = _ok_dict
    ths_mod.THS_Trans2DataFrame = lambda r: r
    ths_mod.THS_EDB = _ok_dict
    ths_mod.THS_QuotesPushing = _ok_dict
    ths_mod.THS_UnQuotesPushing = _ok_dict
    sys.modules["iFinDPy"] = ths_mod

    # WindPy 模块，导出 w
    wind_mod = types.ModuleType("WindPy")
    wind_mod.w = FakeWindClient()
    sys.modules["WindPy"] = wind_mod

    # tqcenter 模块（通达信 TQ），导出 tq + tqconst
    tq_mod = types.ModuleType("tqcenter")
    tq_mod.tq = FakeTdxClient()
    _tqconst = types.SimpleNamespace(STOCK_BUY=0, STOCK_SELL=1, PRICE_MY=0,
                                     PRICE_SJ=1, PRICE_ZTJ=2, PRICE_DTJ=3)
    tq_mod.tqconst = _tqconst
    sys.modules["tqcenter"] = tq_mod

    # xtquant 包 + 子模块（xttrader/xttype/xtconstant）
    xt_pkg = types.ModuleType("xtquant")
    xt_const = types.ModuleType("xtquant.xtconstant")
    xt_const.STOCK_BUY = 23
    xt_const.STOCK_SELL = 24
    xt_const.FIX_PRICE = 11
    xt_const.LATEST_PRICE = 5
    xt_const.SECURITY_ACCOUNT = 2
    xt_const.CREDIT_ACCOUNT = 3
    xt_const.FUTURE_ACCOUNT = 1
    xt_const.HUGANGTONG_ACCOUNT = 6
    xt_const.SHENGANGTONG_ACCOUNT = 7

    xt_trader_mod = types.ModuleType("xtquant.xttrader")
    xt_trader_mod.XtQuantTrader = FakeXtQuantTrader
    xt_trader_mod.XtQuantTraderCallback = FakeXtQuantTraderCallback

    xt_type_mod = types.ModuleType("xtquant.xttype")
    xt_type_mod.StockAccount = FakeStockAccount

    xt_data_mod = types.ModuleType("xtquant.xtdata")
    _fake_xtdata = FakeXtData()
    for _n in ("get_market_data_ex", "get_full_tick", "get_stock_list_in_sector",
               "get_trading_dates", "get_instrument_detail", "download_history_data",
               "subscribe_quote"):
        setattr(xt_data_mod, _n, getattr(_fake_xtdata, _n))

    xt_pkg.xtconstant = xt_const
    xt_pkg.xttrader = xt_trader_mod
    xt_pkg.xttype = xt_type_mod
    xt_pkg.xtdata = xt_data_mod
    sys.modules["xtquant"] = xt_pkg
    sys.modules["xtquant.xtconstant"] = xt_const
    sys.modules["xtquant.xttrader"] = xt_trader_mod
    sys.modules["xtquant.xttype"] = xt_type_mod
    sys.modules["xtquant.xtdata"] = xt_data_mod

    return em_mod, ths_mod, wind_mod


_install_fake_sdks()


@pytest.fixture
def fake_em():
    return sys.modules["EmQuantAPI"].c


@pytest.fixture
def fake_wind():
    return sys.modules["WindPy"].w


@pytest.fixture
def fake_tdx():
    return sys.modules["tqcenter"].tq


@pytest.fixture
def app_client(monkeypatch):
    """构建带鉴权关闭的 TestClient，并重置会话状态。"""
    monkeypatch.setenv("API_KEY", "")
    monkeypatch.setenv("CORS_ORIGINS", "")
    # QMT 桩所需环境：路径/账号/会话号（桩不真连），交易开关默认关、放行非交易时段
    monkeypatch.setenv("QMT_USERDATA_PATH", "X:/fake/userdata_mini")
    monkeypatch.setenv("QMT_ACCOUNT_ID", "test-acct")
    monkeypatch.setenv("QMT_SESSION_ID", "1")
    monkeypatch.setenv("QMT_ALLOW_OFFHOURS", "true")
    monkeypatch.setenv("QMT_TRADING_ENABLED", "false")  # setenv 而非 delenv：抗 load_dotenv setdefault 重灌本机 .env
    monkeypatch.delenv("QMT_CODE_WHITELIST", raising=False)
    monkeypatch.delenv("QMT_MAX_NOTIONAL", raising=False)
    monkeypatch.delenv("QMT_DAILY_ORDER_CAP", raising=False)
    # TDX 交易桩所需环境：账号（桩不真连），交易开关默认关、放行非交易时段
    monkeypatch.setenv("TDX_ACCOUNT_ID", "test-tdx-acct")
    monkeypatch.setenv("TDX_ALLOW_OFFHOURS", "true")
    monkeypatch.setenv("TDX_TRADING_ENABLED", "false")  # setenv 而非 delenv：抗 load_dotenv setdefault 重灌本机 .env
    monkeypatch.delenv("TDX_CODE_WHITELIST", raising=False)
    monkeypatch.delenv("TDX_MAX_NOTIONAL", raising=False)
    monkeypatch.delenv("TDX_DAILY_ORDER_CAP", raising=False)
    # Wind 交易总开关默认关（交易类透传 503，除非用例显式开启）。
    # 用 setenv("false") 而非 delenv：TestClient 启动时 load_dotenv 的 setdefault 会
    # 在 delenv 后把本机 .env 的 WIND_TRADING_ENABLED=true 重新灌回，导致本用例假失败；
    # 显式置 false 后 setdefault 不覆盖已存在值，测试不再受本机 .env 影响。
    monkeypatch.setenv("WIND_TRADING_ENABLED", "false")
    from fastapi.testclient import TestClient
    import importlib
    import stocksdk.guards as guards
    importlib.reload(guards)
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    # 限流器是进程级共享状态（60/60s），不随模块 reload 重置；逐测试清空命中记录，
    # 避免累计请求数跨用例溢出导致 429（多源端点变多后尤其明显）。
    import stocksdk.security as security
    security._limiter._hits.clear()
    import app as app_module
    importlib.reload(app_module)
    return TestClient(app_module.app)
