# 数据存储说明

## PostgreSQL：8 张业务表

| 表名 | 用途 |
|---|---|
| `model_configs` | Chat/Embedding 模型供应商、API、密钥、能力和启用状态 |
| `agents` | 智能体名称、头像、Chat 模型、System Prompt、分类和状态 |
| `knowledge_bases` | 本地知识库名称、描述、状态及其 Embedding 模型 |
| `knowledge_documents` | 上传文件、磁盘存储地址、处理状态和切片数量 |
| `agent_knowledge_bases` | 智能体与本地知识库的多对多关联 |
| `conversations` | 一次对话会话及标题 |
| `messages` | 会话中的用户问题、AI 回答、模型与引用来源 |
| `agent_call_logs` | 模型/API 调用、Token、耗时、费用和异常 |

后端启动时会删除上一版多余表，再自动创建以上 8 张表并初始化 Agent 和模型配置数据。

模型配置关系：

- `agents.chat_model_config_id -> model_configs.id`
- `knowledge_bases.embedding_model_config_id -> model_configs.id`
- 智能体只能选择 `model_type = 'chat'` 的配置。
- 本地知识库只能选择 `model_type = 'embedding'` 的配置。

模型专属字段：

- Embedding：`dimension`、`max_input_tokens`
- Chat：`context_window_tokens`、`max_output_tokens`、`default_temperature`

## Chroma：文档向量

Chroma 本地持久化目录：

```text
storage/chroma
```

Chroma 保存：

- 文档切片正文
- Embedding 向量
- `document_id`
- `knowledge_base_id`
- 文件名、切片位置等来源信息

每个本地知识库对应一个 Chroma collection。删除知识库时会同时删除其 collection。

## 文件存储

上传的原始文件保存在：

```text
storage/knowledge/<knowledge_base_id>/
```

PostgreSQL 的 `knowledge_documents.storage_path` 保存文件绝对路径。

## 模型作用范围

模型使用范围：

- 上传本地文档时使用知识库的 Embedding 模型。
- 图片文档和本地 RAG 问答使用系统默认的 Chat 模型。
- 智能体使用自身关联的 Chat 模型。
- 外部 Agent 向量库不读取、不修改这些模型配置。

## 首次创建数据库

在 CMD 中执行：

```cmd
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U postgres -d postgres -f scripts\init_postgres.sql
```

然后启动：

```cmd
python -m uvicorn app.main:app --reload --port 8000
```

查看实际表：

```cmd
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -U yapmitai -d yapmitai -c "\dt"
```
