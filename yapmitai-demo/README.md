# 悦普 AI 前端

当前版本是零依赖 ES Module 前端，使用 Node.js 内置 HTTP 服务运行。

## 目录结构

页面目录严格对应浏览器 URL：

```text
src/
├── pages/
│   ├── home/index.js
│   ├── enterprise/
│   │   ├── dashboard/index.js
│   │   ├── agents/index.js
│   │   ├── tools/
│   │   │   ├── index.js
│   │   │   ├── agent-config/index.js
│   │   │   └── agent-logs/index.js
│   │   ├── creation/agent/index.js
│   │   ├── outreach/agent/index.js
│   │   ├── personalwx/agent/index.js
│   │   ├── corpwx/agent/index.js
│   │   └── knowledge/agent/index.js
│   ├── talent/home/index.js
│   ├── government/dashboard/index.js
│   └── alliance/dashboard/index.js
├── routes/index.js
├── shared/
│   ├── ui.js
│   └── module-config.js
├── data/mock.js
├── services/agentGatewayService.js
├── static-app.js
└── styles.css
```

## 文件作用

### `src/pages`

每个页面的 `index.js` 包含：

- 页面 URL
- 布局类型
- 该页面的真实渲染代码

页面实现不再集中写在 `static-app.js`。

### `src/routes/index.js`

导入全部页面并生成统一路由表。

### `src/shared/ui.js`

跨页面共享的面板、指标卡、图表、进度条、状态和开关。

### `src/shared/module-config.js`

创作、拓客、个微、企微配置页共用的配置表单。

### `src/data/mock.js`

Demo 阶段的企业、员工、工具、政府、联盟和日志数据。

### `src/services/agentGatewayService.js`

Agent Gateway 前端接口封装。联调时在这里加入 HTTP 请求和 API Key。

### `src/services/knowledgeApi.js`

企业智库后端适配层，封装本地知识库列表、新增、详情、更新、删除和集合上传接口。

企业智库页面采用双栏结构：

- 外部 Agent 向量库：同步状态、向量条目和索引集合
- 本地知识库：表格管理、添加弹窗、文本/图片类型、上传集合、详情、删除和分页
- 外部向量库栏提供 Embedding 模型和回答生成模型切换按钮

### `src/static-app.js`

精简后的应用入口，只负责：

- 路由加载
- 公共后台布局
- 浏览器历史
- 跨页面状态
- 全局交互事件

### `src/styles.css`

全局主题、布局、组件和响应式样式。

## 前后端映射

| 前端页面目录 | 后端页面目录 |
|---|---|
| `pages/enterprise/dashboard` | `app/pages/enterprise/dashboard` |
| `pages/enterprise/agents` | `app/pages/enterprise/agents` |
| `pages/enterprise/tools` | `app/pages/enterprise/tools` |
| `pages/enterprise/tools/agent-config` | `app/pages/enterprise/tools/agent_config` |
| `pages/enterprise/tools/agent-logs` | `app/pages/enterprise/tools/agent_logs` |
| `pages/enterprise/creation/agent` | `app/pages/enterprise/creation/agent` |
| `pages/enterprise/outreach/agent` | `app/pages/enterprise/outreach/agent` |
| `pages/enterprise/personalwx/agent` | `app/pages/enterprise/personalwx/agent` |
| `pages/enterprise/corpwx/agent` | `app/pages/enterprise/corpwx/agent` |
| `pages/enterprise/knowledge/agent` | `app/pages/enterprise/knowledge/agent` |
| `pages/talent/home` | `app/pages/talent/home` |
| `pages/government/dashboard` | `app/pages/government/dashboard` |
| `pages/alliance/dashboard` | `app/pages/alliance/dashboard` |

## 启动

完整步骤见 [`FRONTEND_STARTUP.md`](FRONTEND_STARTUP.md)。

```powershell
cd F:\code\YP\yapmitai-demo
npm.cmd run dev
```

访问：`http://localhost:5173`

## 验证

```powershell
npm.cmd run build
```

该命令检查 Mock 数据和全部页面路由。
