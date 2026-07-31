"""话术分类路由：CRUD、分类下话术数量统计"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Category, Script

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


# ---------- Pydantic 请求/响应模型（本路由专属） ----------


class CategoryCreate(BaseModel):
    """创建分类"""

    name: str
    type: str = ""
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    """更新分类（字段均可选，仅更新传入字段）"""

    name: str | None = None
    type: str | None = None
    sort_order: int | None = None


class CategoryOut(BaseModel):
    """分类输出（含话术数量）"""

    id: int
    name: str
    type: str
    sort_order: int
    script_count: int
    created_at: datetime
    updated_at: datetime


# ---------- 辅助函数 ----------


def _script_count(db: Session, category_id: int) -> int:
    """该分类下的话术数量"""
    return (
        db.scalar(
            select(func.count()).select_from(Script).where(Script.category_id == category_id)
        )
        or 0
    )


def _to_out(db: Session, category: Category) -> CategoryOut:
    """ORM 对象 → 输出模型（补充分类下话术数量）"""
    return CategoryOut(
        id=category.id,
        name=category.name,
        type=category.type,
        sort_order=category.sort_order,
        script_count=_script_count(db, category.id),
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


def _check_name_conflict(db: Session, name: str, exclude_id: int | None = None) -> None:
    """校验分类名称唯一，重名抛 400"""
    stmt = select(Category).where(Category.name == name)
    if exclude_id is not None:
        stmt = stmt.where(Category.id != exclude_id)
    if db.scalar(stmt) is not None:
        raise HTTPException(status_code=400, detail="分类名称已存在")


# ---------- 接口 ----------


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """分类列表（按 sort_order 排序，含各分类话术数量）"""
    categories = db.scalars(
        select(Category).order_by(Category.sort_order, Category.id)
    ).all()
    return [_to_out(db, c) for c in categories]


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """新建分类"""
    _check_name_conflict(db, payload.name)
    category = Category(name=payload.name, type=payload.type, sort_order=payload.sort_order)
    db.add(category)
    db.commit()
    db.refresh(category)
    return _to_out(db, category)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    """更新分类（仅更新传入字段）"""
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="分类不存在")

    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        _check_name_conflict(db, data["name"], exclude_id=category_id)

    for key, value in data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return _to_out(db, category)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """删除分类（分类下仍有话术时拒绝删除）"""
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="分类不存在")

    count = _script_count(db, category_id)
    if count > 0:
        raise HTTPException(status_code=400, detail=f"该分类下仍有 {count} 条话术，无法删除")

    db.delete(category)
    db.commit()
    return None
