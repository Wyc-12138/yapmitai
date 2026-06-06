# 悦普 AI 后端说明文档

`yapmitai-backend` 是“悦普 AI 产业超级操作系统 Demo 2.0”的后端项目。

后端按照说明书指定的技术栈开发，不是 Spring Boot：

- 开发语言：Python 3.12
- Web 框架：FastAPI
- 数据校验：Pydantic
- ORM：SQLAlchemy
- 关系数据库：PostgreSQL
- 缓存：Redis
- 向量数据库：ChromaDB
- HTTP 客户端：httpx
- 测试框架：Pytest
- 接口文档：Swagger / OpenAPI
- 容器编排：Docker Compose

## 一、项目能力

当前后端包含以下能力：

- 企业控制台数据接口
- 超级 AI 员工列表、启停、任务分配和调用
- AI 工具中心
- Agent Gateway 全局配置和模块配置
- 文生图、文生视频 Agent 接口
- 智能获客和 AI 外呼接口
- 个微、企微客服 Webhook
- 企业知识库同步和查询
- Agent 调用日志及统计
- 员工工作台
- 政府驾驶舱和政策问答
- 产业联盟管理
- API Key 鉴权
- 统一响应和统一异常处理
- Agent 调用失败自动降级到 Mock 数据

## 二、项目结构

```text
yapmitai-backend/
├── app/
│   ├── pages/         # 按前端页面路由组织的正式业务入口
│   ├── core/          # 全局配置、响应体、业务异常
│   ├── db/            # PostgreSQL、Redis、ChromaDB 客户端
│   ├── middleware/    # API Key 鉴权和调用日志中间件
│   ├── models/        # SQLAlchemy 数据库模型
│   ├── routers/       # 现有 Router 底层实现
│   ├── schemas/       # 现有 Schema 底层实现及公共模型
│   ├── services/      # 现有 Service 底层实现及共享服务
│   └── main.py        # FastAPI 应用入口
├── tests/             # 自动化测试
├── .env               # 本地环境变量
├── .env.example       # 环境变量模板
├── Dockerfile         # 后端镜像构建配置
├── docker-compose.yml # API、PostgreSQL、Redis、ChromaDB 编排
├── pyproject.toml     # Pytest 和 Ruff 配置
└── requirements.txt   # Python 依赖版本
```

### 页面优先目录

后端正式入口现在与前端 URL 层级一一对应：

```text
app/pages/
├── enterprise/
│   ├── dashboard/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   ├── agents/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   ├── tools/
│   │   ├── router/
│   │   ├── service/
│   │   ├── schema/
│   │   ├── agent_config/
│   │   │   ├── router/
│   │   │   ├── service/
│   │   │   └── schema/
│   │   └── agent_logs/
│   │       ├── router/
│   │       ├── service/
│   │       └── schema/
│   ├── creation/agent/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   ├── outreach/agent/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   ├── personalwx/agent/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   ├── corpwx/agent/
│   │   ├── router/
│   │   ├── service/
│   │   └── schema/
│   └── knowledge/agent/
│       ├── router/
│       ├── service/
│       └── schema/
├── talent/home/
│   ├── router/
│   ├── service/
│   └── schema/
├── government/dashboard/
│   ├── router/
│   ├── service/
│   └── schema/
└── alliance/dashboard/
    ├── router/
    ├── service/
    └── schema/
```

Python 包名不能包含连字符，因此前端 URL 中的：

- `agent-config` 在代码中写为 `agent_config`
- `agent-logs` 在代码中写为 `agent_logs`

每个最终页面目录固定包含：

- `router/`：该页面对应的 HTTP API
- `service/`：该页面的业务逻辑
- `schema/`：该页面的请求和响应参数

`app/pages/__init__.py` 是新的总路由入口，`app/main.py` 从这里加载全部页面模块。

## 三、根目录文件作用

### `README.md`

当前说明文档，介绍项目架构、文件职责、启动方式和接口规则。

### `requirements.txt`

声明后端全部 Python 依赖及固定版本。

其中 `fastapi==0.115.9` 是为了兼容 `chromadb==1.0.12`，不要单独升级 FastAPI，否则可能再次出现依赖冲突。

### `.env`

本机开发环境实际使用的配置，包括 API Key、数据库地址、Redis 地址、ChromaDB 地址和 Agent Gateway 地址。

该文件包含环境相关信息，已被 `.gitignore` 排除，不应提交真实密钥。

### `.env.example`

环境变量示例文件。部署新环境时，应复制为 `.env`，再填写真实配置。

### `.gitignore`

指定 Git 不应提交的文件，例如：

- `.env`
- Python 字节码
- `__pycache__`
- Pytest 缓存
- 虚拟环境
- 测试覆盖率文件

### `Dockerfile`

定义 FastAPI 后端镜像：

1. 使用 Python 3.12 基础镜像。
2. 安装 `requirements.txt`。
3. 复制 `app` 目录。
4. 使用 Uvicorn 启动后端。

### `docker-compose.yml`

一键编排四个服务：

- `api`：FastAPI 后端，端口 `8000`
- `postgres`：PostgreSQL，端口 `5432`
- `redis`：Redis，端口 `6379`
- `chroma`：ChromaDB，宿主机端口 `8001`

同时声明 PostgreSQL 和 ChromaDB 的持久化数据卷。

### `pyproject.toml`

开发工具配置：

- 指定 Pytest 测试目录
- 开启 Pytest 异步模式
- 设置 Ruff 的 Python 版本和单行长度

## 四、应用入口

### `app/__init__.py`

标记 `app` 为 Python 包。

### `app/main.py`

整个后端的启动入口，主要职责：

- 创建 FastAPI 应用
- 配置应用名称和版本
- 配置 CORS
- 注册 API Key 鉴权中间件
- 注册调用日志中间件
- 挂载全部 `/api/v1` 路由
- 注册业务异常、HTTP 异常、参数校验异常和未知异常处理器
- 提供 `/health` 健康检查接口

启动命令中的 `app.main:app` 就是指向该文件中的 `app` 对象。

## 五、核心公共模块

### `app/core/__init__.py`

标记 `core` 为 Python 包。

### `app/core/config.py`

读取和管理环境变量。

主要配置包括：

- 应用名称和运行环境
- API 前缀
- API Key
- Agent Gateway 地址和 Token
- Agent 超时时间
- PostgreSQL、Redis、ChromaDB 地址
- Mock fallback 开关
- CORS 白名单

`get_settings()` 使用缓存，避免每次请求重复读取环境变量。

### `app/core/responses.py`

生成统一接口响应。

成功响应：

```json
{
  "code": 200,
  "data": {},
  "msg": "success",
  "traceId": "uuid"
}
```

失败响应也保持相同结构，只改变 `code`、`msg` 和 HTTP 状态码。

### `app/core/exceptions.py`

定义系统业务异常：

- `AppError`：业务异常基类
- `AgentUnavailableError`：`4001`，Agent 不可用
- `InsufficientBalanceError`：`4002`，余额不足
- `InvalidParameterError`：`4003`，业务参数错误
- `GatewayTimeoutError`：`5001`，Agent Gateway 超时

## 六、数据库与基础设施

### `app/db/__init__.py`

标记 `db` 为 Python 包。

### `app/db/postgres.py`

创建 SQLAlchemy 异步数据库引擎和会话工厂。

`get_db()` 可作为 FastAPI 依赖注入函数，为接口提供 `AsyncSession`。

### `app/db/redis.py`

根据 `REDIS_URL` 创建异步 Redis 客户端。

后续可用于：

- 缓存 Agent Gateway Token
- 保存异步任务状态
- 保存临时配置
- 限流和分布式锁

### `app/db/chroma.py`

创建 ChromaDB HTTP 客户端，用于连接向量数据库。

后续企业知识库的文本向量、相似度查询和 RAG 数据可通过该客户端操作。

## 七、中间件

### `app/middleware/__init__.py`

标记 `middleware` 为 Python 包。

### `app/middleware/auth.py`

API Key 鉴权中间件。

所有 `/api/v1` 接口必须携带：

```text
X-API-Key: yap_demo_key_2026
```

密钥不正确时返回 HTTP `401`。`/health` 和 `/docs` 不受该中间件限制。

### `app/middleware/call_logging.py`

记录每次 `/api/v1` 请求的：

- 请求时间
- 响应时间
- 请求路径
- HTTP 方法
- 成功或失败状态
- 响应耗时

目前 Demo 阶段先保存在内存 `CALL_LOG_STORE` 中，最多保留 200 条。正式环境可改为写入 PostgreSQL 的 `agent_call_logs` 表。

## 八、数据库模型

### `app/models/__init__.py`

统一导出数据库基类和模型，方便 Alembic 或其他模块加载全部表定义。

### `app/models/base.py`

定义 SQLAlchemy 声明式模型基类 `Base`。

所有数据库模型都应继承该类。

### `app/models/agent_call_log.py`

定义 `agent_call_logs` 数据表，字段包括：

- `id`
- `agent_id`
- `module`
- `request_at`
- `response_at`
- `status`
- `latency_ms`
- `cost`
- `error_msg`

## 九、Schema 数据模型

`schemas` 目录负责请求参数校验和接口数据结构声明，不处理业务逻辑。

### `app/schemas/__init__.py`

标记 `schemas` 为 Python 包。

### `app/schemas/common.py`

公共数据模型：

- `ApiResponse`：统一响应泛型
- `ToggleRequest`：通用开关请求
- `Pagination`：分页参数
- `AgentCallRequest`：通用 Agent 调用参数

### `app/schemas/dashboard.py`

企业控制台概览数据结构，包括 KPI、销售趋势、任务分布、任务列表和 Gateway 统计。

### `app/schemas/agent_config.py`

Agent 配置数据结构：

- `GatewayConfigUpdate`：网关地址、超时和全局开关
- `ModuleConfigUpdate`：模块来源和模块参数

### `app/schemas/agents.py`

超级 AI 员工数据结构：

- 创建员工任务
- 单 Agent 启停
- 全局 Agent 启停

### `app/schemas/tools.py`

AI 工具启停请求。

### `app/schemas/creation.py`

AI 创作请求：

- 文生图 Prompt、风格、尺寸和质量
- 文生视频 Prompt、时长、分辨率和语言

### `app/schemas/outreach.py`

AI 拓客请求：

- 线索搜索条件
- AI 外呼联系人、话术和合规确认

### `app/schemas/personalwx.py`

个微客服消息模型，包括联系人、消息内容和接管模式。

### `app/schemas/corpwx.py`

企微客服消息模型，比个微额外包含部门字段。

### `app/schemas/knowledge.py`

企业知识库数据结构：

- 知识查询内容和返回数量
- 知识库同步来源

### `app/schemas/logs.py`

调用日志筛选条件，包括模块和状态。

### `app/schemas/government.py`

政府驾驶舱政策问答请求。

### `app/schemas/alliance.py`

产业联盟成员创建请求，包括企业名称、类型和 AI 等级。

### `app/schemas/talent.py`

员工工作台 AI 助手请求，包括助手名称和用户问题。

## 十、Service 业务层

`services` 目录负责业务处理、Mock 数据加工和外部 Agent 调用，不直接定义 HTTP 路由。

### `app/services/__init__.py`

标记 `services` 为 Python 包。

### `app/services/mock_data.py`

集中存放 Demo 使用的静态数据：

- 企业 KPI
- 销售趋势
- 今日任务
- AI 员工
- AI 工具
- 政府驾驶舱指标
- 联盟计划和联盟成员

正式接入数据库后，可逐步替换这些 Mock 数据。

### `app/services/gateway.py`

统一 Agent Gateway 调用服务。

处理流程：

1. 获取 Gateway URL 和 Token。
2. 使用 httpx 调用外部 Agent。
3. 根据配置执行超时控制。
4. 调用成功时返回真实结果。
5. 未配置 Token、超时或网络异常时返回 Mock fallback。

返回结果会包含 `fallback` 字段，前端可据此提示用户当前使用的是降级数据。

### `app/services/dashboard.py`

组装企业控制台所需的 KPI、趋势图、任务队列、任务分布和 Gateway 统计。

### `app/services/agent_config.py`

管理 Agent Gateway 和各模块配置。

目前配置保存在内存中，包括：

- Gateway 地址
- 超时时间
- 全局开关
- 创作、拓客、个微、企微、知识库模块来源
- 连接测试结果

正式环境可改为 PostgreSQL 或 Redis 持久化。

### `app/services/agents.py`

超级 AI 员工业务逻辑：

- 查询员工列表
- 查询员工详情
- 单员工启停
- 全局启停
- 创建员工任务

### `app/services/tools.py`

AI 工具中心业务逻辑，包括工具查询、分类筛选和启停。

### `app/services/creation.py`

AI 创作业务：

- 调用文生图 Agent
- 提交文生视频任务
- 查询视频任务状态
- 外部服务不可用时返回占位图片或 Mock 视频任务

### `app/services/outreach.py`

AI 拓客业务：

- 搜索企业线索
- 创建 AI 外呼任务
- 生成 Mock 线索
- 将请求转发给 Agent Gateway

### `app/services/personalwx.py`

个微客服回复业务，将收到的消息发送到个微客服 Agent，并支持 Mock fallback。

### `app/services/corpwx.py`

企微客服回复业务，处理部门归属并调用企微客服 Agent。

### `app/services/knowledge.py`

企业知识库业务：

- 创建同步任务
- 查询同步进度
- 查询知识库状态
- 执行合并检索

当前 Demo 使用内存任务状态和 Mock 查询结果，后续可接入 ChromaDB 和 PostgreSQL。

### `app/services/logs.py`

读取中间件产生的调用日志，并计算：

- 调用总数
- 成功率
- 平均耗时
- 费用

### `app/services/government.py`

政府驾驶舱业务：

- 返回宏观 KPI
- 返回产业活跃度数据
- 返回企业类型分布
- 回答政策问题

### `app/services/alliance.py`

产业联盟业务：

- 返回联盟概览
- 返回 AI 增长计划
- 返回联盟成员
- 新增联盟成员

### `app/services/talent.py`

员工工作台业务：

- 返回可用 AI 助手
- 返回本周任务和节省时间
- 调用指定员工助手

## 十一、页面式 Router 接口层

`app/pages` 按前端页面组织正式入口。每个页面的 `router/` 负责接收 HTTP 请求、校验参数、调用 Service，并返回统一响应。

### `app/pages/__init__.py`

创建总路由 `api_router`，注册全部业务路由。

所有路由最终统一挂载到 `/api/v1`。

当前各页面目录中的 `router/`、`service/`、`schema/` 会复用原有横向模块中的实现，保证重构目录时接口行为不发生变化。后续新增或修改页面，应优先在对应的 `app/pages/<前端路由>/` 下开发。

### `app/routers/dashboard.py`

企业控制台：

- `GET /api/v1/dashboard/overview`

### `app/routers/agent_config.py`

Agent 配置：

- `GET /api/v1/agent-config/gateway`
- `PUT /api/v1/agent-config/gateway`
- `POST /api/v1/agent-config/connection-test`
- `GET /api/v1/agent-config/modules/{module}`
- `PUT /api/v1/agent-config/modules/{module}`

### `app/routers/agents.py`

超级 AI 员工：

- `GET /api/v1/agents`
- `GET /api/v1/agents/status`
- `GET /api/v1/agents/{agent_id}`
- `PATCH /api/v1/agents/{agent_id}/toggle`
- `POST /api/v1/agents/global-toggle`
- `POST /api/v1/agents/{agent_id}/tasks`
- `POST /api/v1/agents/{agent_id}/call`

### `app/routers/tools.py`

AI 工具中心：

- `GET /api/v1/tools`
- `PATCH /api/v1/tools/{tool_id}/toggle`

### `app/routers/creation.py`

AI 创作：

- `POST /api/v1/creation/image`
- `POST /api/v1/creation/video`
- `GET /api/v1/creation/video/{task_id}`

### `app/routers/outreach.py`

AI 拓客：

- `POST /api/v1/outreach/leads`
- `POST /api/v1/outreach/calls`

外呼请求必须携带 `consentFlag: true`。

### `app/routers/personalwx.py`

个微客服：

- `POST /api/v1/personalwx/webhook`

### `app/routers/corpwx.py`

企微客服：

- `POST /api/v1/corpwx/webhook`

### `app/routers/knowledge.py`

企业知识库：

- `POST /api/v1/knowledge/sync`
- `GET /api/v1/knowledge/sync/{task_id}`
- `GET /api/v1/knowledge/status`
- `POST /api/v1/knowledge/query`

### `app/routers/logs.py`

调用日志和统计：

- `GET /api/v1/logs`
- `GET /api/v1/stats/overview`
- `GET /api/v1/stats/trend`
- `GET /api/v1/stats/distribution`

### `app/routers/talent.py`

员工工作台：

- `GET /api/v1/talent/home`
- `POST /api/v1/talent/assistant`

### `app/routers/government.py`

政府驾驶舱：

- `GET /api/v1/government/dashboard`
- `POST /api/v1/government/policy-question`

### `app/routers/alliance.py`

产业联盟：

- `GET /api/v1/alliance/dashboard`
- `POST /api/v1/alliance/members`

## 十二、测试文件

### `tests/__init__.py`

标记 `tests` 为 Python 测试包。

### `tests/test_health.py`

测试：

- `/health` 是否正常
- `/api/v1` 是否要求 API Key
- 携带正确 API Key 后企业控制台是否正常返回

### `tests/test_agents.py`

测试：

- AI 员工列表
- AI 员工任务分配
- 未配置 Gateway Token 时文生图是否自动 fallback

## 十三、前后端页面映射

| 前端路由 | 后端业务域 | 主要接口 |
|---|---|---|
| `/enterprise/dashboard` | `dashboard` | `/api/v1/dashboard/overview` |
| `/enterprise/agents` | `agents` | `/api/v1/agents` |
| `/enterprise/tools` | `tools` | `/api/v1/tools` |
| `/enterprise/tools/agent-config` | `agent_config` | `/api/v1/agent-config/*` |
| `/enterprise/creation/agent` | `creation` | `/api/v1/creation/*` |
| `/enterprise/outreach/agent` | `outreach` | `/api/v1/outreach/*` |
| `/enterprise/personalwx/agent` | `personalwx` | `/api/v1/personalwx/*` |
| `/enterprise/corpwx/agent` | `corpwx` | `/api/v1/corpwx/*` |
| `/enterprise/knowledge/agent` | `knowledge` | `/api/v1/knowledge/*` |
| `/enterprise/tools/agent-logs` | `logs` | `/api/v1/logs`、`/api/v1/stats/*` |
| `/talent/home` | `talent` | `/api/v1/talent/*` |
| `/government/dashboard` | `government` | `/api/v1/government/*` |
| `/alliance/dashboard` | `alliance` | `/api/v1/alliance/*` |

## 十四、本地启动

进入后端目录：

```powershell
cd F:\code\YP\yapmitai-backend
```

推荐创建虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

启动后端：

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问地址：

- 健康检查：`http://localhost:8000/health`
- Swagger：`http://localhost:8000/docs`
- OpenAPI JSON：`http://localhost:8000/openapi.json`

## 十五、Docker 启动

电脑安装 Docker Desktop 后执行：

```powershell
cd F:\code\YP\yapmitai-backend
docker compose up --build
```

服务地址：

- FastAPI：`http://localhost:8000`
- PostgreSQL：`localhost:5432`
- Redis：`localhost:6379`
- ChromaDB：`http://localhost:8001`

## 十六、接口调用示例

```powershell
$headers = @{
  "X-API-Key" = "yap_demo_key_2026"
}

Invoke-RestMethod `
  -Uri "http://localhost:8000/api/v1/dashboard/overview" `
  -Headers $headers
```

分配 AI 员工任务：

```powershell
$headers = @{
  "X-API-Key" = "yap_demo_key_2026"
  "Content-Type" = "application/json"
}

$body = @{
  description = "生成海南椰子水东南亚市场增长方案"
  priority = "high"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/api/v1/agents/1/tasks" `
  -Headers $headers `
  -Body $body
```

## 十七、运行测试

```powershell
python -m pytest
```

只运行某个测试文件：

```powershell
python -m pytest tests\test_agents.py -v
```

## 十八、开发约定

新增业务功能时按照前端路由创建目录，并保持三层对应：

```text
app/pages/<frontend-route>/
├── router/
├── service/
└── schema/
```

职责划分：

- `router/`：HTTP 路由、参数接收和状态码
- `schema/`：请求及响应数据校验
- `service/`：业务逻辑、数据库操作和外部 Agent 调用
- Model：PostgreSQL 表结构

不要把复杂业务逻辑直接写进 Router。

## 十九、自动生成文件

运行 Python 后出现的 `__pycache__/` 和 `*.pyc` 是 Python 自动生成的字节码缓存，不属于业务源码，也不需要手工修改。
