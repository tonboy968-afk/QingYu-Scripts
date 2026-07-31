"""数据模型：店铺(Store)、话术分类(Category)、话术(Script)、店铺售后规则(StoreRule)"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Store(Base):
    """店铺"""

    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    platform: Mapped[str] = mapped_column(String(32), default="")
    notes: Mapped[str] = mapped_column(String(512), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    scripts: Mapped[list[Script]] = relationship(back_populates="store")
    rules: Mapped[list[StoreRule]] = relationship(back_populates="store")


class Category(Base):
    """话术分类"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(16), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    scripts: Mapped[list[Script]] = relationship(back_populates="category")


class Script(Base):
    """话术"""

    __tablename__ = "scripts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128))
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(String(256), default="")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    store_id: Mapped[int | None] = mapped_column(
        ForeignKey("stores.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    category: Mapped[Category] = relationship(back_populates="scripts")
    store: Mapped[Store | None] = relationship(back_populates="scripts")


class StoreRule(Base):
    """店铺售后规则（分店铺差异化售后策略）"""

    __tablename__ = "store_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), index=True)
    rule_type: Mapped[str] = mapped_column(String(16), default="备注")
    title: Mapped[str] = mapped_column(String(128))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    store: Mapped[Store] = relationship(back_populates="rules")
