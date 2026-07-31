# 多店铺客服话术管理系统 (MVP)

可视化面板 + 话术归类 + 快速搜索 + 分店铺售后规则的客服话术管理系统。
MVP 聚焦：**系统化管理归类，用户打开软件后能快速精准找到自己想要的话术**。

## 目录结构

```
backend/               # FastAPI 后端
  app/
    main.py            # 应用入口（路由注册、CORS、健康检查）
    db.py              # SQLAlchemy 引擎 / 会话 / 建表
    models.py          # Store / Category / Script / StoreRule
    schemas.py         # Pydantic 基础输出模型
    routers/           # 各资源路由（前缀 /api/v1/...）
  scripts/
    seed.py            # 种子数据（可重复执行）
frontend/              # Vue3 + Element Plus 前端（US-005 起创建）
requirements.txt
```

## 后端启动

```bash
pip install -r requirements.txt
cd backend
python scripts/seed.py        # 首次初始化种子数据（可重复执行）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

- 健康检查: `GET http://127.0.0.1:8010/api/v1/health`
- API 文档: `http://127.0.0.1:8010/docs`
- 数据库: `backend/data/kefu.db`（SQLite，自动建表）
- **注意**：后端端口为 **8010**（本机 8000 被 Windows 系统服务 svchost 占用）

## 数据模型

| 表 | 说明 | 关键字段 |
|----|------|----------|
| stores | 店铺 | name, platform, notes |
| categories | 话术分类 | name, type(售前/售后/申诉/技术), sort_order |
| scripts | 话术 | title, content, tags, category_id, store_id(可空) |
| store_rules | 店铺售后规则 | store_id, rule_type(退款/运费/时效/纠纷/备注), title, content |

## 种子数据

内置 3 个示例店铺、5 大话术分类（单产品售前话术 / 售后通用话术 / 产品售后纠缠话术 / 后台申诉话术 / 产品技术类话术）、13 条示例话术、5 条分店铺售后规则。

## 扩展点（后续迭代预留）

- **API 优先**：所有接口走 `/api/v1/...`，天然满足"预留 API 接口"
- **模型接入 / MCP / 知识库**：计划在 `app/config.py` 配置模型，`app/services/ai.py` 提供话术纠错/润化服务（US-010 落地占位实现）
