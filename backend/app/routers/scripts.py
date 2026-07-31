"""话术路由（US-003 实现具体接口）"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/scripts", tags=["scripts"])
