"""Pydantic 请求/响应模型

约定：各路由的专属请求/响应模型尽量定义在对应 routers/*.py 内部，
避免多个 worker 并行修改本文件造成冲突。这里只放通用基类与基础输出模型。
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """支持从 ORM 对象直接构造响应"""

    model_config = ConfigDict(from_attributes=True)


class StoreOut(ORMModel):
    id: int
    name: str
    platform: str
    notes: str
    created_at: datetime
    updated_at: datetime


class CategoryOut(ORMModel):
    id: int
    name: str
    type: str
    sort_order: int
    created_at: datetime
    updated_at: datetime


class ScriptOut(ORMModel):
    id: int
    title: str
    content: str
    tags: str
    category_id: int
    store_id: int | None
    created_at: datetime
    updated_at: datetime


class StoreRuleOut(ORMModel):
    id: int
    store_id: int
    rule_type: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
