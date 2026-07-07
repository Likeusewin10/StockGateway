"""股票数据 HTTP 服务：其他项目通过 ip:端口 + 参数取数，无需写 SDK 代码。

启动（在 .venv-api 下）：
    .venv-api\\Scripts\\python -m uvicorn app:app --host 0.0.0.0 --port 8000

说明：
- 两个 SDK 均单会话/单点登录，本服务用全局锁串行化所有请求，
  必须单 worker 运行（不要加 --workers）。
- 经 ngrok 公网暴露：务必配置 API_KEY；取数端点已加按 IP 限流。
- 交互式文档：http://<ip>:8000/docs

实现已拆分到 stocksdk 包：config / sessions / serialize / security /
routes_em / routes_ths / routes_ws。本文件仅负责装配。
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stocksdk.config import get_api_key, get_cors_origins, load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("stocksdk")

# 路由依赖 SDK，须在 .env 加载后导入
from stocksdk import routes_downloads, routes_em, routes_health, routes_qmt, routes_tdx, routes_ths, routes_wind, routes_ws  # noqa: E402


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    if not get_api_key():
        logger.warning("未配置 API_KEY：取数接口当前不鉴权，请勿暴露到公网")
    if not _cors_origins:
        logger.info("未配置 CORS_ORIGINS：默认拒绝跨域请求")
    logger.info("服务已启动，限流与鉴权依赖已装配")
    yield


app = FastAPI(title="股票数据服务", description="EM + iFinD + Wind + TDX 取数 + QMT 交易统一接口", lifespan=_lifespan)

# CORS：默认拒绝跨域；CORS_ORIGINS 显式配置白名单才放开。
_cors_origins = get_cors_origins()
if _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["X-API-Key", "Content-Type"],
    )

app.include_router(routes_em.router)
app.include_router(routes_ths.router)
app.include_router(routes_wind.router)
app.include_router(routes_tdx.router)
app.include_router(routes_qmt.router)
app.include_router(routes_ws.router)
app.include_router(routes_health.router)
app.include_router(routes_downloads.router)


@app.get("/health")
def health():
    return {"status": "ok"}
