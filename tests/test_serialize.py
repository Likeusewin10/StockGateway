"""单元测试：serialize（SDK 返回值归一化）。"""
import pandas as pd
import pytest
from fastapi import HTTPException

from stocksdk import serialize


class _Obj:
    def __init__(self, error_code=0, error_msg="", data=None):
        self.ErrorCode = error_code
        self.ErrorMsg = error_msg
        self.Data = data


def test_em_result_dataframe_to_records():
    df = pd.DataFrame({"a": [1, 2]})
    out = serialize.em_result(df)
    assert out == [{"index": 0, "a": 1}, {"index": 1, "a": 2}]


def test_em_result_tuple_unwraps_dataframe():
    df = pd.DataFrame({"a": [1]})
    out = serialize.em_result((0, df))
    assert out == [{"index": 0, "a": 1}]


def test_em_result_error_raises_502():
    with pytest.raises(HTTPException) as exc:
        serialize.em_result(_Obj(error_code=10001, error_msg="boom"))
    assert exc.value.status_code == 502


def test_em_result_object_returns_data():
    assert serialize.em_result(_Obj(error_code=0, data={"k": 1})) == {"k": 1}


def test_ths_result_dataframe():
    df = pd.DataFrame({"b": [9]})
    assert serialize.ths_result(df) == [{"index": 0, "b": 9}]


def test_ths_result_error_dict_raises_502():
    with pytest.raises(HTTPException) as exc:
        serialize.ths_result({"errorcode": 5, "errmsg": "bad"})
    assert exc.value.status_code == 502


def test_ths_result_ok_dict_passthrough():
    d = {"errorcode": 0, "tables": [1]}
    assert serialize.ths_result(d) is d


def test_em_quote_to_dict_ok():
    qd = _Obj(error_code=0)
    qd.Codes = ["300059.SZ"]
    qd.Indicators = ["now"]
    qd.Data = {"now": [1.0]}
    out = serialize.em_quote_to_dict(qd)
    assert out["event"] == "quote"
    assert out["codes"] == ["300059.SZ"]


def test_em_quote_to_dict_error():
    out = serialize.em_quote_to_dict(_Obj(error_code=7, error_msg="x"))
    assert out["event"] == "error"
    assert out["code"] == 7


def test_merge_pandas_option_appends_to_options_string():
    out = serialize.merge_pandas_option(["code", "TradeDate=20240105"], True)
    assert out[-1] == "TradeDate=20240105,Ispandas=1"


def test_merge_pandas_option_skips_non_option_last_arg():
    # 最后一个是日期，不含 '='，不应追加
    out = serialize.merge_pandas_option(["300059.SZ", "2024-01-05"], True)
    assert out == ["300059.SZ", "2024-01-05"]


def test_merge_pandas_option_does_not_mutate_input():
    original = ["code", "X=1"]
    serialize.merge_pandas_option(original, True)
    assert original == ["code", "X=1"]


def test_merge_pandas_option_disabled():
    out = serialize.merge_pandas_option(["X=1"], False)
    assert out == ["X=1"]
