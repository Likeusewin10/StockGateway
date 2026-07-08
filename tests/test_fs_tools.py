"""文件传输核心逻辑单测（mcp_gateway/fs_tools.py）。

全程 tmp_path，纯本地磁盘，不碰网络/网关进程。覆盖：
二进制往返（\\r\\n \\x00 高位字节）、append 分块、fs_stat 终验、MSYS 路径归一、
相对路径/非法 base64/非法 mode/负 offset 拒绝、mkdirs 开关、offset/max_bytes 分块
读边界（跨 EOF / offset 超长）、单次写入超上限、不存在文件读取失败。
"""
import base64
import hashlib
import os

import pytest

import mcp_gateway.fs_tools as ft
from mcp_gateway.fs_tools import fs_get_impl, fs_put_impl, fs_stat_impl

# 含 CRLF / NUL / 高位字节的 payload：任何换行或编码转换都会改变 sha256
BINARY_PAYLOAD = b"\x00\x01binary\r\nline\nmix\xff\xfe\x80" * 100


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ---- fs_put ----

def test_put_write_roundtrip(tmp_path):
    target = tmp_path / "blob.bin"
    res = fs_put_impl(str(target), b64(BINARY_PAYLOAD))
    assert res["ok"] is True
    assert res["bytes_written"] == len(BINARY_PAYLOAD)
    assert res["size"] == len(BINARY_PAYLOAD)
    assert res["sha256"] == sha(BINARY_PAYLOAD)
    assert target.read_bytes() == BINARY_PAYLOAD


def test_put_write_truncates_existing(tmp_path):
    target = tmp_path / "blob.bin"
    target.write_bytes(b"old-content-longer-than-new")
    res = fs_put_impl(str(target), b64(b"new"))
    assert res["ok"] is True
    assert target.read_bytes() == b"new"


def test_put_append_chunks_reassemble(tmp_path):
    target = tmp_path / "big.bin"
    chunks = [BINARY_PAYLOAD[i:i + 1000] for i in range(0, len(BINARY_PAYLOAD), 1000)]
    first = fs_put_impl(str(target), b64(chunks[0]), mode="write")
    assert first["sha256"] == sha(chunks[0])  # write 模式回整文件哈希
    for chunk in chunks[1:]:
        res = fs_put_impl(str(target), b64(chunk), mode="append")
        assert res["ok"] is True
        assert res["sha256"] is None  # append 不整文件重哈希（O(n²)），终验走 fs_stat
    assert target.read_bytes() == BINARY_PAYLOAD
    assert res["size"] == len(BINARY_PAYLOAD)
    stat = fs_stat_impl(str(target))
    assert stat["sha256"] == sha(BINARY_PAYLOAD)


def test_put_append_expected_size_guard(tmp_path):
    """expected_size 幂等保护：重试重复追加同一块会被拒绝并回报当前 size。"""
    target = tmp_path / "chunked.bin"
    fs_put_impl(str(target), b64(b"AAAA"), mode="write")
    res = fs_put_impl(str(target), b64(b"BBBB"), mode="append", expected_size=4)
    assert res["ok"] is True and res["size"] == 8
    # 模拟超时重试：同一块再发一次，expected_size 仍是 4，须被拒绝
    retry = fs_put_impl(str(target), b64(b"BBBB"), mode="append", expected_size=4)
    assert retry["ok"] is False
    assert retry["size"] == 8  # 回报当前 size 供调用方重新对齐
    assert target.read_bytes() == b"AAAABBBB"  # 文件未被污染


def test_put_append_expected_size_on_missing_file(tmp_path):
    """目标不存在时视为 0 字节：expected_size=0 放行首块 append。"""
    target = tmp_path / "fresh.bin"
    res = fs_put_impl(str(target), b64(b"x"), mode="append", expected_size=0)
    assert res["ok"] is True and res["size"] == 1


def test_put_mkdirs_creates_parents(tmp_path):
    target = tmp_path / "a" / "b" / "c" / "deep.bin"
    res = fs_put_impl(str(target), b64(b"x"))
    assert res["ok"] is True
    assert target.read_bytes() == b"x"


def test_put_mkdirs_false_missing_parent_fails(tmp_path):
    target = tmp_path / "nosuchdir" / "f.bin"
    res = fs_put_impl(str(target), b64(b"x"), mkdirs=False)
    assert res["ok"] is False
    assert "error" in res
    assert not target.exists()


def test_put_invalid_base64(tmp_path):
    res = fs_put_impl(str(tmp_path / "f.bin"), "not@@valid###b64!!")
    assert res["ok"] is False
    assert "base64" in res["error"]


def test_put_invalid_mode(tmp_path):
    res = fs_put_impl(str(tmp_path / "f.bin"), b64(b"x"), mode="rewrite")
    assert res["ok"] is False
    assert "mode" in res["error"]


def test_put_relative_path_rejected():
    res = fs_put_impl("relative/f.bin", b64(b"x"))
    assert res["ok"] is False
    assert "path" in res["error"]


def test_put_over_size_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "FS_PUT_MAX_BYTES", 10)
    res = fs_put_impl(str(tmp_path / "f.bin"), b64(b"x" * 11))
    assert res["ok"] is False
    assert "append" in res["error"]  # 报错须提示分块


# ---- fs_get ----

def test_get_roundtrip(tmp_path):
    target = tmp_path / "blob.bin"
    target.write_bytes(BINARY_PAYLOAD)
    res = fs_get_impl(str(target))
    assert res["ok"] is True
    assert res["size"] == len(BINARY_PAYLOAD)
    assert res["bytes_read"] == len(BINARY_PAYLOAD)
    assert res["eof"] is True
    assert res["sha256"] == sha(BINARY_PAYLOAD)
    assert base64.b64decode(res["data_b64"]) == BINARY_PAYLOAD


def test_get_chunked_by_offset(tmp_path):
    target = tmp_path / "blob.bin"
    target.write_bytes(BINARY_PAYLOAD)
    parts, offset = [], 0
    while True:
        res = fs_get_impl(str(target), offset=offset, max_bytes=1000)
        assert res["ok"] is True
        chunk = base64.b64decode(res["data_b64"])
        assert res["bytes_read"] == len(chunk)
        assert res["sha256"] == sha(chunk)  # sha256 是本块的
        parts.append(chunk)
        offset += len(chunk)
        if res["eof"]:
            break
    assert b"".join(parts) == BINARY_PAYLOAD


def test_get_offset_past_eof(tmp_path):
    target = tmp_path / "small.bin"
    target.write_bytes(b"abc")
    res = fs_get_impl(str(target), offset=100)
    assert res["ok"] is True
    assert res["bytes_read"] == 0
    assert res["eof"] is True
    assert res["data_b64"] == ""


def test_get_negative_offset_rejected(tmp_path):
    res = fs_get_impl(str(tmp_path / "f.bin"), offset=-1)
    assert res["ok"] is False
    assert "offset" in res["error"]


def test_get_negative_max_bytes_rejected(tmp_path):
    res = fs_get_impl(str(tmp_path / "f.bin"), max_bytes=-1)
    assert res["ok"] is False
    assert "max_bytes" in res["error"]


def test_get_missing_file(tmp_path):
    res = fs_get_impl(str(tmp_path / "nope.bin"))
    assert res["ok"] is False
    assert "error" in res


def test_get_max_bytes_capped_by_server_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(ft, "FS_GET_MAX_BYTES", 5)
    target = tmp_path / "blob.bin"
    target.write_bytes(b"0123456789")
    res = fs_get_impl(str(target), max_bytes=1000)  # 超服务端上限被压回 5
    assert res["ok"] is True
    assert res["bytes_read"] == 5
    assert res["eof"] is False


# ---- fs_stat ----

def test_stat_matches_local_hash(tmp_path):
    target = tmp_path / "blob.bin"
    target.write_bytes(BINARY_PAYLOAD)
    res = fs_stat_impl(str(target))
    assert res["ok"] is True
    assert res["size"] == len(BINARY_PAYLOAD)
    assert res["sha256"] == sha(BINARY_PAYLOAD)


def test_stat_missing_file(tmp_path):
    res = fs_stat_impl(str(tmp_path / "nope.bin"))
    assert res["ok"] is False


# ---- 路径归一 ----

def test_normalize_relative_rejected():
    assert ft._normalize_path("foo/bar") is None
    assert ft._normalize_path("") is None


@pytest.mark.skipif(os.name != "nt", reason="MSYS 盘符归一仅 Windows 语义")
def test_normalize_msys_drive_path(tmp_path):
    # /c/Users/... 与 C:\Users\... 归一到同一路径
    msys = "/" + str(tmp_path)[0].lower() + "/" + str(tmp_path)[3:].replace("\\", "/")
    assert ft._normalize_path(msys) == tmp_path.resolve()


@pytest.mark.skipif(os.name != "nt", reason="Windows 下裸 / 路径无盘符归属")
def test_normalize_bare_posix_root_rejected_on_windows():
    assert ft._normalize_path("/no/drive/here") is None


@pytest.mark.skipif(os.name != "nt", reason="正/反斜杠等价仅 Windows")
def test_put_msys_path_writes_same_file(tmp_path):
    target = tmp_path / "via_msys.bin"
    msys = "/" + str(target)[0].lower() + "/" + str(target)[3:].replace("\\", "/")
    res = fs_put_impl(msys, b64(b"hello"))
    assert res["ok"] is True
    assert target.read_bytes() == b"hello"
