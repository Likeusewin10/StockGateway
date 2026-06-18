"""StockSDK 共享模块：配置、会话、归一化、安全、路由。

仅依赖标准库的子模块（config）可在三个 venv（api/em/ths）下通用导入；
依赖 fastapi/SDK 的子模块仅供 .venv-api 下的 HTTP 服务使用。
"""
