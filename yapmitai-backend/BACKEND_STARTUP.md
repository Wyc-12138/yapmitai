# 后端启动文档

## 1. 环境要求

- Python 3.12
- PostgreSQL 16 或更高版本
- Redis 7，可选；当前主要业务未依赖 Redis 持久化
- 前端默认运行在 `http://localhost:5173`

检查 Python：

```powershell
python --version
```

## 2. 进入后端目录

```powershell
cd F:\code\YP\yapmitai-backend
```

## 3. 创建虚拟环境

首次运行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

以后启动只需激活：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 禁止执行激活脚本：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. 配置环境变量

首次创建 `.env`：

```powershell
Copy-Item .env.example .env
```

关键配置：

```env
API_KEY=yap_demo_key_2026
DATABASE_URL=postgresql+asyncpg://yapmitai:yapmitai@localhost:5432/yapmitai
CORS_ORIGINS=http://localhost:5173
CHROMA_PERSIST_DIR=storage/chroma
KNOWLEDGE_STORAGE_DIR=storage/knowledge
```

模型 API Key 在“模型配置中心”中维护。页面只显示 Key 后四位。

## 5. 准备数据库

先按照 [`POSTGRESQL_SETUP.md`](POSTGRESQL_SETUP.md) 创建数据库和用户。

## 6. 启动后端

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

后端启动时会：

1. 连接 PostgreSQL。
2. 创建或迁移 10 张业务表。
3. 初始化默认智能体和模型配置。
4. 初始化本地 Chroma 持久化目录。

访问地址：

- 健康检查：`http://localhost:8000/health`
- Swagger：`http://localhost:8000/docs`
- OpenAPI：`http://localhost:8000/openapi.json`

## 7. 验证接口

PowerShell：

```powershell
$headers = @{ "X-API-Key" = "yap_demo_key_2026" }
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/model-configs" -Headers $headers
```

## 8. 运行测试

```powershell
python -m pytest -q
```

## 9. 数据存储位置

- PostgreSQL：系统业务数据。
- `storage/chroma`：知识库文档切片和向量。
- `storage/knowledge/<knowledge_base_id>`：用户上传的原始文件。

## 10. Docker Compose 启动

```powershell
docker compose up --build
```

这会启动 API、PostgreSQL 和 Redis。若本机 PostgreSQL 已占用 `5432`，需先停止本机服务或修改 `docker-compose.yml` 端口。

## 11. 常见问题

### 数据库连接失败

确认 PostgreSQL 服务已启动，并检查 `.env` 中的用户名、密码、端口和数据库名。

### 前端请求被 CORS 拒绝

确认：

```env
CORS_ORIGINS=http://localhost:5173
```

修改 `.env` 后重启后端。

### 模型调用失败

进入模型配置页面，检查 API 地址、API Key、模型编码、启用状态和默认状态。

### 停止后端

在启动后端的控制台按 `Ctrl+C`。
