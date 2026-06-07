# 悦普 AI 后端

技术栈：Python 3.12、FastAPI、Pydantic、SQLAlchemy、PostgreSQL、Redis、ChromaDB（本地持久化）、Pytest、Docker Compose。

数据库使用 8 张业务表，完整结构见 [`DATABASE.md`](DATABASE.md)。

## 目录结构

后端业务目录严格对应前端页面：

```text
app/
├── pages/
│   ├── enterprise/
│   │   ├── dashboard/{router,service,schema}/
│   │   ├── agents/{router,service,schema}/
│   │   ├── tools/
│   │   │   ├── router/
│   │   │   ├── service/
│   │   │   ├── schema/
│   │   │   ├── agent_config/{router,service,schema}/
│   │   │   └── agent_logs/{router,service,schema}/
│   │   ├── creation/agent/{router,service,schema}/
│   │   ├── outreach/agent/{router,service,schema}/
│   │   ├── personalwx/agent/{router,service,schema}/
│   │   ├── corpwx/agent/{router,service,schema}/
│   │   └── knowledge/agent/{router,service,schema}/
│   ├── talent/home/{router,service,schema}/
│   ├── government/dashboard/{router,service,schema}/
│   └── alliance/dashboard/{router,service,schema}/
├── shared/
├── core/
├── db/
├── middleware/
├── models/
└── main.py
```

每个最终页面目录包含：

- `router/__init__.py`：HTTP API
- `service/__init__.py`：页面业务逻辑
- `schema/__init__.py`：Pydantic 参数模型

Python 包名不能包含连字符，因此前端的 `agent-config`、`agent-logs` 在后端使用 `agent_config`、`agent_logs`。

## 根目录文件

- `requirements.txt`：Python 依赖。ChromaDB 1.0.12 要求 FastAPI 0.115.9。
- `.env`：本地环境变量。
- `.env.example`：环境变量模板。
- `.gitignore`：排除密钥、虚拟环境和缓存。
- `Dockerfile`：构建 FastAPI 镜像。
- `docker-compose.yml`：编排 API、PostgreSQL 和 Redis；Chroma 随 API 使用本地持久化目录。
- `pyproject.toml`：Pytest 和 Ruff 配置。

## 公共文件

- `app/main.py`：创建 FastAPI、配置 CORS、中间件、异常处理和 `/health`。
- `app/pages/__init__.py`：唯一业务总路由入口。
- `app/shared/gateway.py`：调用 Agent Gateway，处理超时和 Mock fallback。
- `app/shared/external_ai.py`：调用外部 OpenAI 兼容 Embedding、Chat 和图片理解 API。
- `app/shared/mock_data.py`：跨页面共享的 Demo 数据。
- `app/shared/schema.py`：统一响应、分页、开关和通用 Agent 参数。
- `app/core/config.py`：环境变量配置。
- `app/core/responses.py`：统一响应体。
- `app/core/exceptions.py`：业务错误码。
- `app/db/postgres.py`：SQLAlchemy 异步数据库会话。
- `app/db/redis.py`：异步 Redis 客户端。
- `app/db/chroma.py`：Chroma 本地持久化客户端，保存文档切片和 Embedding 向量。
- `app/middleware/auth.py`：`X-API-Key` 鉴权。
- `app/middleware/call_logging.py`：调用日志中间件。
- `app/models/base.py`：SQLAlchemy 模型基类。
- `app/models/agent_call_log.py`：Agent 调用日志表。

## 页面文件作用

### `app/pages/enterprise/dashboard`

- Router：`GET /api/v1/dashboard/overview`
- Service：KPI、销售趋势、任务队列、Gateway 统计
- Schema：控制台概览模型

### `app/pages/enterprise/agents`

- Router：员工列表、详情、启停、任务分配、Agent 调用
- Service：员工状态和任务业务
- Schema：任务、单 Agent 开关、全局开关

### `app/pages/enterprise/tools`

- Router：工具列表和启停
- Service：工具查询和状态更新
- Schema：工具开关参数

### `app/pages/enterprise/tools/agent_config`

- Router：Gateway 配置、模块配置、连接测试
- Service：配置状态管理
- Schema：Gateway 和模块配置

### `app/pages/enterprise/tools/agent_logs`

- Router：日志、调用概览、趋势、分布
- Service：日志筛选和统计
- Schema：日志筛选参数

### `app/pages/enterprise/creation/agent`

- Router：文生图、文生视频、视频状态
- Service：创作 Agent 和 fallback
- Schema：图片及视频生成参数

### `app/pages/enterprise/outreach/agent`

- Router：线索搜索和 AI 外呼
- Service：拓客 Agent 调用
- Schema：行业、地区、关键词、联系人和合规参数

### `app/pages/enterprise/personalwx/agent`

- Router：个微 Webhook
- Service：个微客服 Agent
- Schema：联系人、消息和接管模式

### `app/pages/enterprise/corpwx/agent`

- Router：企微 Webhook
- Service：企微客服 Agent
- Schema：联系人、部门、消息和接管模式

### `app/pages/enterprise/knowledge/agent`

- Router：外部向量库同步、本地知识库 CRUD、集合上传和知识查询
- Service：同步任务、本地知识库管理和合并检索
- Schema：同步来源、查询、本地知识库创建和更新参数

本地知识库接口：

```text
GET    /api/v1/knowledge/local-libraries
POST   /api/v1/knowledge/local-libraries
GET    /api/v1/knowledge/local-libraries/{library_id}
PATCH  /api/v1/knowledge/local-libraries/{library_id}
DELETE /api/v1/knowledge/local-libraries/{library_id}
POST   /api/v1/knowledge/local-libraries/{library_id}/collections
```

模型配置接口：

```text
GET /api/v1/knowledge/model-config
PUT /api/v1/knowledge/model-config
```

外部模型环境变量：

```text
EXTERNAL_AI_BASE_URL=https://api.openai.com/v1
EXTERNAL_AI_API_KEY=
EMBEDDING_MODELS=text-embedding-3-small,text-embedding-3-large
ANSWER_MODELS=gpt-4o-mini,gpt-4.1-mini
```

模型按钮会真实调用 `EXTERNAL_AI_BASE_URL` 提供的 OpenAI 兼容
`/embeddings` 和 `/chat/completions` 接口，不使用本地模拟结果。必须在
`.env` 填写真实的 `EXTERNAL_AI_API_KEY` 并重启后端。

企业智库页面可针对具体本地知识库保存模型配置，并执行“测试 Embedding +
回答模型”。成功时会显示向量维度、真实回答和 Token，失败时显示上游 API
返回的错误。

文本上传流程：

```text
文本提取 → 500 字符切分 → 50 字符重叠 → 外部 Embedding API
```

图片上传流程：

```text
外部多模态回答模型生成图片描述 → 外部 Embedding API
```

问答流程：

```text
知识检索上下文 → 外部回答模型生成答案
```

### `app/pages/talent/home`

- Router：员工工作台和 AI 助手
- Service：员工助手业务
- Schema：助手名称和 Prompt

### `app/pages/government/dashboard`

- Router：驾驶舱和政策问答
- Service：政府 KPI、企业分布、政策回答
- Schema：政策问题

### `app/pages/alliance/dashboard`

- Router：联盟看板和成员新增
- Service：联盟概览、增长计划、成员业务
- Schema：联盟成员参数

## 前后端映射

| 前端路由 | 后端目录 |
|---|---|
| `/enterprise/dashboard` | `app/pages/enterprise/dashboard` |
| `/enterprise/agents` | `app/pages/enterprise/agents` |
| `/enterprise/tools` | `app/pages/enterprise/tools` |
| `/enterprise/tools/agent-config` | `app/pages/enterprise/tools/agent_config` |
| `/enterprise/tools/agent-logs` | `app/pages/enterprise/tools/agent_logs` |
| `/enterprise/creation/agent` | `app/pages/enterprise/creation/agent` |
| `/enterprise/outreach/agent` | `app/pages/enterprise/outreach/agent` |
| `/enterprise/personalwx/agent` | `app/pages/enterprise/personalwx/agent` |
| `/enterprise/corpwx/agent` | `app/pages/enterprise/corpwx/agent` |
| `/enterprise/knowledge/agent` | `app/pages/enterprise/knowledge/agent` |
| `/talent/home` | `app/pages/talent/home` |
| `/government/dashboard` | `app/pages/government/dashboard` |
| `/alliance/dashboard` | `app/pages/alliance/dashboard` |

## 启动

```powershell
cd F:\code\YP\yapmitai-backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

- 健康检查：`http://localhost:8000/health`
- Swagger：`http://localhost:8000/docs`
- API Key：`X-API-Key: yap_demo_key_2026`

## 测试

```powershell
python -m pytest
```

- `tests/test_health.py`：健康检查、鉴权、控制台
- `tests/test_agents.py`：员工、任务和 fallback

## 开发规则

新增页面时创建：

```text
app/pages/<frontend-route>/
├── router/
├── service/
└── schema/
```

业务写在 `service`，参数写在 `schema`，`router` 只处理 HTTP。
