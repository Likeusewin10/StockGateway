# StockSDK 部署说明

两个股票数据 SDK 各自用独立的 Python venv（均为 Python 3.11.4 x64）。

## SDK 2：同花顺 iFinD（已跑通）

```bat
py -3.11 -m venv .venv-ths
.venv-ths\Scripts\activate
pip install -r requirements-ths.txt
python verify_ths.py
```

- 凭据来自 `.env`（`THS_USER` / `THS_PWD`），不入库、不硬编码。
- 注意：同花顺单点登录，勿在多处同时登录同一账号。

## SDK 1：东方财富 EMQuantAPI

SDK 文件位于 `D:\dev\Project\EMQuantAPI_Python\python3`（不复制进本项目，venv 通过 `.pth` 引用）。

```bat
py -3.11 -m venv .venv-em
.venv-em\Scripts\activate
:: 注册接口（在 venv 激活态下运行）
cd /d D:\dev\Project\EMQuantAPI_Python\python3
python installEmQuantAPI.py
cd /d D:\dev\Project\StockSDK
```

运行依赖：Microsoft Visual C++ 2010 可再发行组件包（x64，本机已装）。

### 激活（生成 userInfo 令牌，需绑定手机号的 Choice 账号）

运行图形激活工具，输入绑定手机号、获取验证码：

```
D:\dev\Project\EMQuantAPI_Python\python3\libs\windows\LoginActivator.exe
```

激活成功后生成 `userInfo` 令牌文件。然后：

```bat
.venv-em\Scripts\python verify_em.py
```

- 默认用 userInfo 令牌登录。
- 若想用账密登录（不生成令牌），在 `.env` 增加 `EM_USER` / `EM_PWD` 后再运行。

## 安全

- `.env`、`userInfo`、`docs/quantapi/相关信息.txt` 已被 `.gitignore` 排除，不入版本库。
- 代码一律从环境变量 / `.env` 读取凭据，无硬编码。
