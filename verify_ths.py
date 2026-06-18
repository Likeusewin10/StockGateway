"""同花顺 iFinD 登录 + 取数冒烟脚本。

凭据从环境变量读取（THS_USER / THS_PWD），不硬编码。
若存在同目录 .env，则自动加载。

运行：
    .venv-ths\\Scripts\\python verify_ths.py
期望：THS_iFinDLogin 返回 0，THS_HistoryQuotes 返回非空数据。
"""
import os
import sys
from pathlib import Path


def load_dotenv():
    """极简 .env 加载：KEY=value 逐行，忽略空行与 # 注释。"""
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def main():
    load_dotenv()
    user = os.environ.get("THS_USER")
    pwd = os.environ.get("THS_PWD")
    if not user or not pwd:
        print("ERROR: 缺少环境变量 THS_USER / THS_PWD（检查 .env）")
        return 1

    from iFinDPy import (
        THS_iFinDLogin,
        THS_HistoryQuotes,
        THS_iFinDLogout,
    )

    code = THS_iFinDLogin(user, pwd)
    print("THS_iFinDLogin ->", code)
    if code != 0:
        print("登录失败，按官网手册/错误码排查（权限、单点登录冲突、出网白名单）")
        return 1

    try:
        df = THS_HistoryQuotes(
            "300033.SZ",
            "open;high;low;close",
            "",
            "2024-01-01",
            "2024-01-05",
        )
        print("THS_HistoryQuotes ->")
        print(df)
    finally:
        THS_iFinDLogout()
    return 0


if __name__ == "__main__":
    sys.exit(main())
