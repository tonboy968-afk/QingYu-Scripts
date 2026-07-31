"""店铺售后规则路由：CRUD、按店铺过滤、类型枚举校验"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Store, StoreRule

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])

# 售后规则类型枚举
RULE_TYPES = {"退款", "运费", "时效", "纠纷", "备注"}


# ---------- Pydantic 请求/响应模型（本路由专属） ----------


class RuleCreate(BaseModel):
    """创建售后规则"""

    store_id: int
    rule_type: str = "备注"
    title: str
    content: str = ""


class RuleUpdate(BaseModel):
    """更新售后规则（字段均可选，仅更新传入字段）"""

    store_id: Optional[int] = None
    rule_type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None


class RuleOut(BaseModel):
    """售后规则输出（含店铺名）"""

    id: int
    store_id: int
    store_name: Optional[str] = None
    rule_type: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


# ---------- 辅助函数 ----------


def _to_out(rule: StoreRule) -> RuleOut:
    """ORM 对象 → 输出模型（补充店铺名）"""
    return RuleOut(
        id=rule.id,
        store_id=rule.store_id,
        store_name=rule.store.name if rule.store else None,
        rule_type=rule.rule_type,
        title=rule.title,
        content=rule.content,
        created_at=rule.created_at,
        updated_at=rule.updated_at,
    )


def _check_store(db: Session, store_id: int) -> None:
    """校验店铺存在性，不存在抛 400"""
    if db.get(Store, store_id) is None:
        raise HTTPException(status_code=400, detail="店铺不存在")


def _check_rule_type(rule_type: str) -> None:
    """校验规则类型枚举，非法值抛 400"""
    if rule_type not in RULE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"规则类型非法，可选值：{'/'.join(sorted(RULE_TYPES))}",
        )


def _get_rule_or_404(db: Session, rule_id: int) -> StoreRule:
    """获取规则，不存在抛 404"""
    rule = db.get(StoreRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="售后规则不存在")
    return rule


# ---------- 接口 ----------


@router.get("", response_model=list[RuleOut])
def list_rules(
    store_id: Optional[int] = Query(None, description="按店铺过滤"),
    db: Session = Depends(get_db),
):
    """售后规则列表（可选按店铺过滤，按更新时间倒序）"""
    stmt = select(StoreRule)
    if store_id is not None:
        stmt = stmt.where(StoreRule.store_id == store_id)
    rules = db.scalars(stmt.order_by(StoreRule.updated_at.desc(), StoreRule.id.desc())).all()
    return [_to_out(r) for r in rules]


@router.post("", response_model=RuleOut, status_code=201)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    """新建售后规则"""
    _check_store(db, payload.store_id)
    _check_rule_type(payload.rule_type)
    rule = StoreRule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _to_out(rule)


@router.get("/{rule_id}", response_model=RuleOut)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    """售后规则详情"""
    return _to_out(_get_rule_or_404(db, rule_id))


@router.put("/{rule_id}", response_model=RuleOut)
def update_rule(rule_id: int, payload: RuleUpdate, db: Session = Depends(get_db)):
    """更新售后规则（仅更新传入字段）"""
    rule = _get_rule_or_404(db, rule_id)

    data = payload.model_dump(exclude_unset=True)
    if "store_id" in data and data["store_id"] is not None:
        _check_store(db, data["store_id"])
    if "rule_type" in data and data["rule_type"] is not None:
        _check_rule_type(data["rule_type"])

    for key, value in data.items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return _to_out(rule)


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    """删除售后规则"""
    rule = _get_rule_or_404(db, rule_id)
    db.delete(rule)
    db.commit()
    return None
