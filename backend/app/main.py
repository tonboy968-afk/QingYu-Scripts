"""多店铺客服话术管理系统 - FastAPI 入口"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routers import categories, dashboard, rules, scripts, stores


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="多店铺客服话术管理系统 API",
    description=(
        "客服话术管理：话术分类、快速检索、分店铺售后规则；"
        "预留 AI 模型接入 / MCP / 知识库扩展点"
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# 前端 dev server 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stores.router)
app.include_router(categories.router)
app.include_router(scripts.router)
app.include_router(rules.router)
app.include_router(dashboard.router)


@app.get("/api/v1/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
