# 悦普 AI 前端说明

这是悦普 AI 产业超级操作系统 Demo 2.0 前端。

## 技术说明

当前版本为零依赖 ES Module 静态前端，可直接使用 Node.js 内置 HTTP 服务运行，不需要下载安装第三方 npm 包。

## 页面目录

前端页面目录严格对应浏览器 URL：

```text
src/
├── pages/
│   ├── home/
│   │   └── index.js
│   ├── enterprise/
│   │   ├── dashboard/
│   │   │   └── index.js
│   │   ├── agents/
│   │   │   └── index.js
│   │   ├── tools/
│   │   │   ├── index.js
│   │   │   ├── agent-config/
│   │   │   │   └── index.js
│   │   │   └── agent-logs/
│   │   │       └── index.js
│   │   ├── creation/agent/
│   │   │   └── index.js
│   │   ├── outreach/agent/
│   │   │   └── index.js
│   │   ├── personalwx/agent/
│   │   │   └── index.js
│   │   ├── corpwx/agent/
│   │   │   └── index.js
│   │   └── knowledge/agent/
│   │       └── index.js
│   ├── talent/home/
│   │   └── index.js
│   ├── government/dashboard/
│   │   └── index.js
│   └── alliance/dashboard/
│       └── index.js
├── routes/
│   └── index.js
├── data/
│   └── mock.js
├── services/
│   └── agentGatewayService.js
├── static-app.js
└── styles.css
```

## 目录职责

### `src/pages`

页面入口层。每个 `index.js` 声明：

- 页面 URL
- 页面使用全屏布局还是后台布局
- 页面对应的渲染器

### `src/routes/index.js`

统一导入所有页面入口，生成前端路由表，并提供 `findRoute()` 进行页面匹配。

### `src/data/mock.js`

存放 Demo 阶段使用的企业、员工、工具、政府、联盟和调用日志数据。

### `src/services/agentGatewayService.js`

前端 Agent Gateway API 服务封装。后续前后端联调时，在这里统一加入真实 HTTP 请求、API Key 和异常 fallback。

### `src/static-app.js`

前端运行入口，负责：

- 根据路由加载页面
- 处理导航和浏览器历史
- 提供公共布局和页面渲染器
- 处理筛选、抽屉、弹窗、开关等交互

### `src/styles.css`

全局深色主题、响应式布局、页面组件和动画样式。

## 前后端对应

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

后端 Python 包名不能使用连字符，因此后端使用 `agent_config` 和 `agent_logs`。

## 启动

```powershell
cd F:\code\YP\yapmitai-demo
npm.cmd run dev
```

访问：

```text
http://localhost:5173
```

## 验证

```powershell
npm.cmd run build
```

该命令会检查关键文件、Mock 数据以及全部页面路由是否注册完整。
