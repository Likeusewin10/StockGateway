"""东方财富 EMQuantAPI 登录 + 取数冒烟脚本。

默认使用 userInfo 令牌登录（需先用 LoginActivator.exe 激活生成 userInfo）。
若设置了环境变量 EM_USER / EM_PWD，则改用账密登录（不生成令牌）。

运行：
    .venv-em\\Scripts\\python verify_em.py
期望：start ErrorCode=0，csd 返回非空 Data。
"""
import os
import sys
from pathlib import Path


def load_dotenv():
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
    from EmQuantAPI import c

    user = os.environ.get("EM_USER")
    pwd = os.environ.get("EM_PWD")
    if user and pwd:
        # 账密登录模式（不生成 userInfo 令牌）
        options = "ForceLogin=1,UserName={},Password={}".format(user, pwd)
    else:
        # 令牌登录模式（已激活生成 userInfo）
        options = "ForceLogin=1"

    r = c.start(options, "")
    print("c.start -> ErrorCode={} ErrorMsg={}".format(r.ErrorCode, r.ErrorMsg))
    if r.ErrorCode != 0:
        print("登录失败，按错误码排查："
              "10001002 账密错误 / 10001003-04 无权限 / "
              "10001009 登录数超限 / 10001019 设备不一致 / 10001020 令牌失效")
        return 1

    try:
        data = c.csd("300059.SZ", "CLOSE", "2024-01-01", "2024-01-05", "")
        print("c.csd -> ErrorCode={}".format(data.ErrorCode))
        print("Data:", data.Data)
        if data.ErrorCode != 0 or not data.Data:
            print("取数失败/为空：", data.ErrorMsg)
            return 1
    finally:
        c.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
