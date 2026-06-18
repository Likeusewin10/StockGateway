"""单元测试：config（.env 加载与设置）。"""
from stocksdk import config


def test_load_dotenv_parses_keys(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("FOO=bar\n# comment\n\nBAZ = qux \n", encoding="utf-8")
    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.delenv("BAZ", raising=False)

    config.load_dotenv(env)

    import os
    assert os.environ["FOO"] == "bar"
    assert os.environ["BAZ"] == "qux"


def test_load_dotenv_missing_file_is_silent(tmp_path):
    config.load_dotenv(tmp_path / "nope.env")  # 不抛异常即通过


def test_load_dotenv_does_not_override_existing(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("PRESET=fromfile\n", encoding="utf-8")
    monkeypatch.setenv("PRESET", "fromenv")

    config.load_dotenv(env)

    import os
    assert os.environ["PRESET"] == "fromenv"


def test_get_cors_origins(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://a.com, https://b.com ,")
    assert config.get_cors_origins() == ["https://a.com", "https://b.com"]
    monkeypatch.setenv("CORS_ORIGINS", "")
    assert config.get_cors_origins() == []


def test_require_ths_credentials(monkeypatch):
    monkeypatch.setenv("THS_USER", "u")
    monkeypatch.setenv("THS_PWD", "p")
    assert config.require_ths_credentials() == ("u", "p")
    monkeypatch.delenv("THS_USER", raising=False)
    import pytest
    with pytest.raises(RuntimeError):
        config.require_ths_credentials()
