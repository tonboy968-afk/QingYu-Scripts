"""话术分类路由（US-002 实现具体接口）"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])
