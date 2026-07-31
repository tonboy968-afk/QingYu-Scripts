<div align="center">

<img src="https://img.shields.io/badge/version-v0.1.0-blue.svg" alt="Version">
<img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
<img src="https://img.shields.io/badge/backend-FastAPI-009688.svg" alt="FastAPI">
<img src="https://img.shields.io/badge/frontend-Vue3%20%7C%20Element--Plus-42B883.svg" alt="Vue3">
<img src="https://img.shields.io/badge/database-SQLite-003B57.svg" alt="SQLite">

# 青语话术 · QingYu Scripts

**多店铺客服话术管理与快速检索系统**

*可视化看板 · 话术归类 · 快速搜索 · 分店铺售后规则 · AI 智能润色*

[快速开始](#-快速开始) · [核心特性](#-核心特性) · [架构设计](#-架构设计) · [贡献指南](#-贡献指南)

</div>

---

## 📖 项目简介

**青语话术（QingYu Scripts）** 是一款专为电商客服团队打造的**话术管理与快速检索系统**。通过系统化的分类、店铺化的售后规则、可视化的数据看板，让客服人员**打开软件即可快速精准找到需要的话术**，告别在 Word / 微信聊天记录中翻找的历史。

作为 **QingYu Agent**（青语智能客服）的配套项目，青语话术聚焦"知识沉淀 + 快速检索"这一独立场景，与 QingYu Agent 的"自动回复"形成完整闭环：

- 📚 **话术库**：系统化整理历史话术、模板、规则
- 🔍 **快速检索**：分类 / 关键词 / 标签多维度检索
- 🏪 **店铺隔离**：不同店铺独立售后规则（退款/运费/时效/纠纷）
- 🎨 **可视化看板**：数据一目了然，深色模式 + 企业级 Admin 布局
- 🤖 **AI 增强**：预留模型接入，话术纠错 / 润色（占位实现）

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📂 **5 大话术分类** | 单产品售前 / 售后通用 / 产品售后纠缠 / 后台申诉 / 产品技术 |
| 🏪 **多店铺管理** | 不同店铺独立售后规则，支持店铺筛选与动画切换 |
| 📋 **店铺售后规则** | 退款 / 运费 / 时效 / 纠纷 / 备注 五类规则按店铺隔离 |
| 🔍 **多维度检索** | 分类 + 关键词 + 标签 + 店铺组合查询 |
| 🌙 **深色模式** | 完整深色主题，长时间工作更护眼 |
| 🎨 **模块化看板** | 企业级 Admin 布局，数据可视化、状态卡片 |
| ⚡ **一键启动** | `启动.bat` 双击即可运行完整系统 |
| 🤖 **AI 接入占位** | 预留话术纠错 / 润色接口（可接入 OpenAI / Qwen / 本地 LLM） |

---
### 目录结构

```
qinyu-scripts/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 应用入口（路由注册、CORS、健康检查）
│   │   ├── db.py              # SQLAlchemy 引擎 / 会话 / 建表
│   │   ├── models.py          # Store / Category / Script / StoreRule
│   │   ├── schemas.py         # Pydantic 数据模型
│   │   ├── config.py          # 配置（模型接入预留）
│   │   └── routers/           # 各资源路由（/api/v1/...）
│   ├── scripts/
│   │   └── seed.py            # 种子数据（可重复执行）
│   └── data/                  # SQLite 数据文件
├── frontend/                   # Vue3 + Element Plus 前端
│   ├── src/
│   │   ├── views/             # 仪表盘 / 话术 / 分类 / 店铺 / 规则
│   │   ├── components/        # 通用组件
│   │   ├── router/            # 路由配置
│   │   └── api/               # 后端 API 封装
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── progress_notes/             # 开发进度与用户故事文档
├── requirements.txt
├── 启动.bat                   # Windows 一键启动脚本
├── prd.json                   # 产品需求文档
├── task.md                    # 任务清单
└── README.md
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- Windows 10+ / macOS / Linux

### 方式一：一键启动（推荐 Windows 用户）

双击项目根目录的 `启动.bat`，脚本会自动：
1. 创建 Python 虚拟环境并安装依赖
2. 启动后端服务（端口 8010）
3. 启动前端开发服务器（端口 5173）
4. 打开浏览器访问

### 方式二：手动启动

#### 启动后端

```bash
pip install -r requirements.txt
cd backend
python scripts/seed.py        # 首次初始化种子数据（可重复执行）
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

#### 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端界面 | http://localhost:5173 |
| 后端 API | http://127.0.0.1:8010 |
| API 文档（Swagger） | http://127.0.0.1:8010/docs |
| 健康检查 | http://127.0.0.1:8010/api/v1/health |

> ⚠️ **端口说明**：后端默认端口为 **8010**（本机 8000 端口可能被 Windows 系统服务 svchost 占用）

---

## 📊 数据模型

| 表 | 说明 | 关键字段 |
|----|------|----------|
| **stores** | 店铺 | name, platform, notes |
| **categories** | 话术分类 | name, type(售前/售后/申诉/技术), sort_order |
| **scripts** | 话术 | title, content, tags, category_id, store_id(可空) |
| **store_rules** | 店铺售后规则 | store_id, rule_type(退款/运费/时效/纠纷/备注), title, content |

### 种子数据

内置完整示例数据，开箱即可体验：

- ✅ 3 个示例店铺
- ✅ 5 大话术分类
- ✅ 13 条示例话术
- ✅ 5 条分店铺售后规则
- ✅ 5 大通用话术模板（产品售后纠缠场景）

---

## 🔌 API 概览

所有接口前缀：`/api/v1/`

| 模块 | 端点 | 方法 |
|------|------|------|
| 健康检查 | `/health` | GET |
| 店铺管理 | `/stores` | GET / POST / PUT / DELETE |
| 话术分类 | `/categories` | GET / POST / PUT / DELETE |
| 话术 | `/scripts` | GET / POST / PUT / DELETE |
| 店铺售后规则 | `/store-rules` | GET / POST / PUT / DELETE |
| 仪表盘统计 | `/dashboard` | GET |

详细接口文档参见：[Swagger UI](http://127.0.0.1:8010/docs)

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | FastAPI 0.110+ |
| ORM | SQLAlchemy 2.0+ |
| 数据校验 | Pydantic 2.6+ |
| 数据库 | SQLite 3 |
| 前端框架 | Vue 3.4+ |
| UI 组件库 | Element Plus 2.14+ |
| 路由 | Vue Router 4.6+ |
| HTTP 客户端 | Axios 1.19+ |
| 构建工具 | Vite 5.0+ |

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 需要帮助的方向

| 领域 | 任务 | 难度 |
|------|------|------|
| 🤖 **AI 接入** | 接入 OpenAI / Qwen / 本地 LLM 实现话术润色 | ⭐⭐⭐ |
| 📊 **数据分析** | 话术使用频率统计、转化率分析 | ⭐⭐ |
| 🔍 **全文检索** | 集成 SQLite FTS5 或 Elasticsearch | ⭐⭐⭐ |
| 📱 **多端适配** | 移动端 H5 / 小程序 | ⭐⭐ |
| 🎨 **UI 优化** | 更多可视化图表、看板组件 | ⭐ |
| 🧪 **测试覆盖** | 单元测试、E2E 测试 | ⭐⭐ |
| 📝 **文档** | 用户手册、视频教程 | ⭐ |

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交改动 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

---

## 🗺️ 路线图

- [x] ✅ **v0.1.0 MVP** - 多店铺话术管理、5 大分类、店铺售后规则、深色看板
- [ ] 🚧 **v0.2.0** - AI 话术润色与纠错（模型接入）
- [ ] 📋 **v0.3.0** - 全文检索与高级筛选
- [ ] 📋 **v0.4.0** - 数据看板与转化分析
- [ ] 📋 **v1.0.0** - 与 QingYu Agent 深度集成（自动话术匹配）

---


## 🔗 相关项目

- **[QingYu Agent](https://github.com/tonboy968-afk/qing-yu-agent)** - Workflow + Policy 双引擎驱动的多平台智能客服 Agent

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star 支持一下！**

[报告 Bug](https://github.com/tonboy968-afk/qinyu-scripts/issues) · [功能建议](https://github.com/tonboy968-afk/qinyu-scripts/issues)

</div>
