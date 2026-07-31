"""店铺管理路由：CRUD、店铺下话术/规则数量统计"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Script, Store, StoreRule

router = APIRouter(prefix="/api/v1/stores", tags=["stores"])


# ---------- Pydantic 请求/响应模型（本路由专属） ----------


class StoreCreate(BaseModel):
    """创建店铺"""

    name: str
    platform: str = ""
    notes: str = ""


class StoreUpdate(BaseModel):
    """更新店铺（字段均可选，仅更新传入字段）"""

    name: str | None = None
    platform: str | None = None
    notes: str | None = None


class StoreOut(BaseModel):
    """店铺输出（含话术数量与规则数量）"""

    id: int
    name: str
    platform: str
    notes: str
    script_count: int
    rule_count: int
    created_at: datetime
    updated_at: datetime


# ---------- 辅助函数 ----------


def _counts(db: Session, store_id: int) -> tuple[int, int]:
    """店铺下的话术数量与售后规则数量"""
    script_count = (
        db.scalar(
            select(func.count()).select_from(Script).where(Script.store_id == store_id)
        )
        or 0
    )
    rule_count = (
        db.scalar(
            select(func.count()).select_from(StoreRule).where(StoreRule.store_id == store_id)
        )
        or 0
    )
    return script_count, rule_count


def _to_out(db: Session, store: Store) -> StoreOut:
    """ORM 对象 → 输出模型（补充话术/规则数量）"""
    script_count, rule_count = _counts(db, store.id)
    return StoreOut(
        id=store.id,
        name=store.name,
        platform=store.platform,
        notes=store.notes,
        script_count=script_count,
        rule_count=rule_count,
        created_at=store.created_at,
        updated_at=store.updated_at,
    )


def _check_name_conflict(db: Session, name: str, exclude_id: int | None = None) -> None:
    """校验店铺名称唯一，重名抛 400"""
    stmt = select(Store).where(Store.name == name)
    if exclude_id is not None:
        stmt = stmt.where(Store.id != exclude_id)
    if db.scalar(stmt) is not None:
        raise HTTPException(status_code=400, detail="店铺名称已存在")


# ---------- 接口 ----------


@router.get("", response_model=list[StoreOut])
def list_stores(db: Session = Depends(get_db)):
    """店铺列表（含话术/规则数量）"""
    stores = db.scalars(select(Store).order_by(Store.id)).all()
    return [_to_out(db, s) for s in stores]


@router.post("", response_model=StoreOut, status_code=201)
def create_store(payload: StoreCreate, db: Session = Depends(get_db)):
    """新建店铺"""
    _check_name_conflict(db, payload.name)
    store = Store(name=payload.name, platform=payload.platform, notes=payload.notes)
    db.add(store)
    db.commit()
    db.refresh(store)
    return _to_out(db, store)


@router.put("/{store_id}", response_model=StoreOut)
def update_store(store_id: int, payload: StoreUpdate, db: Session = Depends(get_db)):
    """更新店铺（仅更新传入字段）"""
    store = db.get(Store, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="店铺不存在")

    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        _check_name_conflict(db, data["name"], exclude_id=store_id)

    for key, value in data.items():
        setattr(store, key, value)
    db.commit()
    db.refresh(store)
    return _to_out(db, store)


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """删除店铺（店铺下仍有话术或售后规则时拒绝删除）"""
    store = db.get(Store, store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="店铺不存在")

    script_count, rule_count = _counts(db, store_id)
    if script_count > 0:
        raise HTTPException(status_code=400, detail=f"该店铺下仍有 {script_count} 条话术，无法删除")
    if rule_count > 0:
        raise HTTPException(status_code=400, detail=f"该店铺下仍有 {rule_count} 条售后规则，无法删除")

    db.delete(store)
    db.commit()
    return None
