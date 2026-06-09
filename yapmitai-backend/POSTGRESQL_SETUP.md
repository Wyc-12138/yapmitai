# PostgreSQL 数据库构建文档

## 1. 数据库信息

默认开发配置：

| 配置 | 值 |
|---|---|
| 主机 | `localhost` |
| 端口 | `5432` |
| 数据库 | `yapmitai` |
| 用户 | `yapmitai` |
| 密码 | `yapmitai` |
| 编码 | `UTF8` |

生产环境必须修改默认密码。

## 2. 创建用户和数据库

### PowerShell

```powershell
cd F:\code\YP\yapmitai-backend
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U postgres -d postgres -f .\scripts\init_postgres.sql
```

### CMD

CMD 中不要输入 PowerShell 的 `&` 和反引号：

```cmd
cd /d F:\code\YP\yapmitai-backend
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U postgres -d postgres -f scripts\init_postgres.sql
```

如果 PostgreSQL 安装版本不是 18，请修改可执行文件路径。

## 3. 创建业务表

配置后端 `.env`：

```env
DATABASE_URL=postgresql+asyncpg://yapmitai:yapmitai@localhost:5432/yapmitai
```

首次启动后端：

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

后端会自动创建、迁移并初始化以下 10 张表：

| 表名 | 用途 |
|---|---|
| `model_configs` | Chat 与 Embedding 模型配置 |
| `agents` | 智能体信息及Chat模型关联 |
| `knowledge_bases` | 本地知识库及Embedding模型关联 |
| `knowledge_documents` | 知识库上传文件和处理状态 |
| `agent_knowledge_bases` | 智能体与知识库关联 |
| `conversations` | 对话会话 |
| `messages` | 会话消息和知识引用 |
| `agent_call_logs` | API与模型调用日志 |
| `ai_tools` | Prompt Skill工具定义和模型配置 |
| `skill_run_records` | AI工具最近运行结果历史 |

## 4. 添加中文表和字段备注

业务表创建完成后执行：

### PowerShell

```powershell
$env:PGPASSWORD="yapmitai"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U yapmitai -d yapmitai -f .\scripts\apply_database_comments.sql
Remove-Item Env:PGPASSWORD
```

### CMD

```cmd
set PGPASSWORD=yapmitai
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U yapmitai -d yapmitai -f scripts\apply_database_comments.sql
set PGPASSWORD=
```

该脚本可重复执行，不会修改业务数据。

## 5. 查看所有表

```powershell
$env:PGPASSWORD="yapmitai"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U yapmitai -d yapmitai -c "\dt+"
Remove-Item Env:PGPASSWORD
```

## 6. 查看表和字段中文备注

查看表备注：

```sql
SELECT
    c.relname AS table_name,
    obj_description(c.oid, 'pg_class') AS table_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
ORDER BY c.relname;
```

查看字段备注：

```sql
SELECT
    c.relname AS table_name,
    a.attname AS column_name,
    col_description(c.oid, a.attnum) AS column_comment
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_attribute a ON a.attrelid = c.oid
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY c.relname, a.attnum;
```

## 7. 表之间的主要关系

```text
agents.chat_model_config_id
  -> model_configs.id

knowledge_bases.embedding_model_config_id
  -> model_configs.id

knowledge_documents.knowledge_base_id
  -> knowledge_bases.id

agent_knowledge_bases.agent_id
  -> agents.id

agent_knowledge_bases.knowledge_base_id
  -> knowledge_bases.id

conversations.agent_id
  -> agents.id

messages.conversation_id
  -> conversations.id
```

## 8. 备份数据库

```powershell
$env:PGPASSWORD="yapmitai"
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -h localhost -U yapmitai -d yapmitai -F c -f .\yapmitai.backup
Remove-Item Env:PGPASSWORD
```

## 9. 恢复数据库

恢复会写入数据库，请先确认目标数据库：

```powershell
$env:PGPASSWORD="yapmitai"
& "C:\Program Files\PostgreSQL\18\bin\pg_restore.exe" -h localhost -U yapmitai -d yapmitai --clean --if-exists .\yapmitai.backup
Remove-Item Env:PGPASSWORD
```

## 10. 重建开发数据库

如果需要彻底重建，应先备份。删除数据库会清空全部 PostgreSQL 业务数据，Chroma 和上传文件需单独处理。

推荐开发流程：

1. 备份现有数据库。
2. 使用管理员账户删除并重新创建 `yapmitai`。
3. 启动后端自动创建业务表。
4. 执行 `apply_database_comments.sql` 添加中文备注。
