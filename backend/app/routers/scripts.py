"""话术路由：CRUD、关键词搜索、分类/店铺/标签筛选、分页"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from ..db import get_db
from ..models import Category, Script, Store

router = APIRouter(prefix="/api/v1/scripts", tags=["scripts"])


# ---------- Pydantic 请求/响应模型（本路由专属） ----------


class ScriptCreate(BaseModel):
    """创建话术"""

    title: str
    content: str
    tags: str = ""
    category_id: int
    store_id: Optional[int] = None


class ScriptUpdate(BaseModel):
    """更新话术（字段均可选，仅更新传入字段）"""

    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    category_id: Optional[int] = None
    store_id: Optional[int] = None


class ScriptOut(BaseModel):
    """话术输出（含分类名/店铺名）"""

    id: int
    title: str
    content: str
    tags: str
    category_id: int
    category_name: Optional[str] = None
    store_id: Optional[int] = None
    store_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ScriptListOut(BaseModel):
    """话术分页列表"""

    total: int
    items: list[ScriptOut]
    page: int
    page_size: int


# ---------- 辅助函数 ----------


def _to_out(script: Script) -> ScriptOut:
    """ORM 对象 → 输出模型（补充分类名/店铺名）"""
    return ScriptOut(
        id=script.id,
        title=script.title,
        content=script.content,
        tags=script.tags,
        category_id=script.category_id,
        category_name=script.category.name if script.category else None,
        store_id=script.store_id,
        store_name=script.store.name if script.store else None,
        created_at=script.created_at,
        updated_at=script.updated_at,
    )


def _check_fk(db: Session, category_id: int | None, store_id: int | None) -> None:
    """校验外键存在性，不存在抛 400"""
    if category_id is not None and db.get(Category, category_id) is None:
        raise HTTPException(status_code=400, detail="分类不存在")
    if store_id is not None and db.get(Store, store_id) is None:
        raise HTTPException(status_code=400, detail="店铺不存在")


# ---------- 接口 ----------


@router.get("", response_model=ScriptListOut)
def list_scripts(
    q: Optional[str] = Query(None, description="关键词，对标题/内容/标签模糊搜索"),
    category_id: Optional[int] = Query(None, description="按分类筛选"),
    store_id: Optional[int] = Query(None, description="按店铺筛选"),
    tag: Optional[str] = Query(None, description="按标签精确匹配（tags 为逗号分隔）"),
    page: int = Query(1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数，上限 100"),
    db: Session = Depends(get_db),
):
    """话术列表：关键词搜索 + 分类/店铺/标签筛选 + 分页"""
    stmt = select(Script).options(joinedload(Script.category), joinedload(Script.store))

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(Script.title.like(like), Script.content.like(like), Script.tags.like(like))
        )
    if category_id is not None:
        stmt = stmt.where(Script.category_id == category_id)
    if store_id is not None:
        stmt = stmt.where(Script.store_id == store_id)
    if tag:
        # 用分隔符包裹 tags 后做精确标签匹配，避免"催"误匹配"催单"
        stmt = stmt.where(func.concat(",", Script.tags, ",").like(f"%,{tag},%"))

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = (
        db.scalars(
            stmt.order_by(Script.updated_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        .all()
    )
    return ScriptListOut(
        total=total, items=[_to_out(s) for s in items], page=page, page_size=page_size
    )


@router.post("", response_model=ScriptOut, status_code=201)
def create_script(payload: ScriptCreate, db: Session = Depends(get_db)):
    """新建话术"""
    _check_fk(db, payload.category_id, payload.store_id)
    script = Script(**payload.model_dump())
    db.add(script)
    db.commit()
    db.refresh(script)
    return _to_out(script)


@router.get("/{script_id}", response_model=ScriptOut)
def get_script(script_id: int, db: Session = Depends(get_db)):
    """话术详情"""
    script = db.get(Script, script_id)
    if script is None:
        raise HTTPException(status_code=404, detail="话术不存在")
    return _to_out(script)


@router.put("/{script_id}", response_model=ScriptOut)
def update_script(script_id: int, payload: ScriptUpdate, db: Session = Depends(get_db)):
    """更新话术（仅更新传入字段；store_id 显式传 null 表示清除店铺绑定）"""
    script = db.get(Script, script_id)
    if script is None:
        raise HTTPException(status_code=404, detail="话术不存在")

    data = payload.model_dump(exclude_unset=True)
    if "category_id" in data:
        _check_fk(db, data["category_id"], None)
    if "store_id" in data and data["store_id"] is not None:
        _check_fk(db, None, data["store_id"])

    for key, value in data.items():
        setattr(script, key, value)
    db.commit()
    db.refresh(script)
    return _to_out(script)


@router.delete("/{script_id}", status_code=204)
def delete_script(script_id: int, db: Session = Depends(get_db)):
    """删除话术"""
    script = db.get(Script, script_id)
    if script is None:
        raise HTTPException(status_code=404, detail="话术不存在")
    db.delete(script)
    db.commit()
    return None
