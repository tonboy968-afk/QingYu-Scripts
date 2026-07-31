"""仪表盘统计路由：话术/分类/店铺/规则总数、分类分布、最近更新话术"""
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from ..db import get_db
from ..models import Category, Script, Store, StoreRule

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


# ---------- Pydantic 响应模型（本路由专属） ----------


class CategoryCountOut(BaseModel):
    """分类分布条目"""

    category_id: int
    name: str
    count: int


class RecentScriptOut(BaseModel):
    """最近更新话术条目"""

    id: int
    title: str
    category_name: str | None = None
    store_name: str | None = None
    updated_at: datetime


class StatsOut(BaseModel):
    """仪表盘统计数据"""

    total_scripts: int
    total_categories: int
    total_stores: int
    total_rules: int
    category_distribution: list[CategoryCountOut]
    recent_scripts: list[RecentScriptOut]


# ---------- 接口 ----------


@router.get("/stats", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    """仪表盘统计：总数 + 分类分布 + 最近更新话术（5 条）"""
    total_scripts = db.scalar(select(func.count()).select_from(Script)) or 0
    total_categories = db.scalar(select(func.count()).select_from(Category)) or 0
    total_stores = db.scalar(select(func.count()).select_from(Store)) or 0
    total_rules = db.scalar(select(func.count()).select_from(StoreRule)) or 0

    dist_rows = db.execute(
        select(Category.id, Category.name, func.count(Script.id))
        .outerjoin(Script, Script.category_id == Category.id)
        .group_by(Category.id)
        .order_by(Category.sort_order, Category.id)
    ).all()
    category_distribution = [
        CategoryCountOut(category_id=cid, name=name, count=count)
        for cid, name, count in dist_rows
    ]

    recent = db.scalars(
        select(Script)
        .options(joinedload(Script.category), joinedload(Script.store))
        .order_by(Script.updated_at.desc())
        .limit(5)
    ).all()
    recent_scripts = [
        RecentScriptOut(
            id=s.id,
            title=s.title,
            category_name=s.category.name if s.category else None,
            store_name=s.store.name if s.store else None,
            updated_at=s.updated_at,
        )
        for s in recent
    ]

    return StatsOut(
        total_scripts=total_scripts,
        total_categories=total_categories,
        total_stores=total_stores,
        total_rules=total_rules,
        category_distribution=category_distribution,
        recent_scripts=recent_scripts,
    )
