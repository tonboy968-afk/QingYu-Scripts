"""店铺售后规则路由（US-004 实现具体接口）"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])
