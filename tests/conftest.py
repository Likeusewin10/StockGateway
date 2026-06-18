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

    return em_mod, ths_mod


_install_fake_sdks()


@pytest.fixture
def fake_em():
    return sys.modules["EmQuantAPI"].c


@pytest.fixture
def app_client(monkeypatch):
    """构建带鉴权关闭的 TestClient，并重置会话状态。"""
    monkeypatch.setenv("API_KEY", "")
    monkeypatch.setenv("CORS_ORIGINS", "")
    from fastapi.testclient import TestClient
    import importlib
    import stocksdk.sessions as sessions
    importlib.reload(sessions)
    import app as app_module
    importlib.reload(app_module)
    return TestClient(app_module.app)
