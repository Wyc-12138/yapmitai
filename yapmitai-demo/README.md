# 悦普 AI 前端

当前版本使用 Vue 3、Vue Router 与 Vite，要求 Node.js 版本大于 22。

## 目录结构

页面目录严格对应浏览器 URL：

```text
src/
├── App.vue
├── layouts/AppShell.vue
├── components/
│   ├── PageHeader.vue
│   ├── AppPanel.vue
│   ├── KpiCard.vue
│   ├── LineChart.vue
│   ├── DonutChart.vue
│   ├── ProgressBar.vue
│   ├── AppToggle.vue
│   └── ModuleConfigPage.vue
├── pages/
│   ├── home/index.vue
│   ├── enterprise/
│   │   ├── dashboard/index.vue
│   │   ├── agents/index.vue
│   │   ├── tools/
│   │   │   ├── index.vue
│   │   │   ├── api/index.js
│   │   │   ├── agent-config/index.vue
│   │   │   └── agent-logs/index.vue
│   │   ├── model-configs/
│   │   │   ├── index.vue
│   │   │   └── api/index.js
│   │   └── knowledge/agent/
│   │       ├── index.vue
│   │       └── api/index.js
│   ├── talent/home/index.vue
│   ├── government/dashboard/index.vue
│   └── alliance/dashboard/index.vue
├── router/index.js
├── data/mock.js
├── main.js
└── styles.css
```

## 文件作用

### `src/main.js`

Vue 3 应用入口，负责：

- 创建 Vue 应用
- 注册 Vue Router
- 挂载根组件

### `src/pages`

每个页面使用标准 Vue 单文件组件 `index.vue`：

- `<template>`：页面结构
- `<script setup>`：状态、方法、请求和生命周期
- `<style scoped>`：页面局部样式

需要调用后端的页面在同级 `api/index.js` 中维护接口，目录层级继续与浏览器 URL 对应。

### `src/router/index.js`

使用 Vue Router 懒加载全部 `index.vue` 页面。

### `src/components`

标准 Vue 公共组件，包括面板、指标卡、图表、进度条、开关和模块配置页面。

### `src/data/mock.js`

Demo 阶段的企业、员工、工具、政府、联盟和日志数据。

### 页面同级 `api/index.js`

AI工具、企业智库和模型配置分别在自己的页面目录中维护后端请求，不再使用集中式 `services` 目录。

企业智库页面采用双栏结构：

- 外部 Agent 向量库：同步状态、向量条目和索引集合
- 本地知识库：表格管理、添加弹窗、文本/图片类型、上传集合、详情、删除和分页
- 本地知识库栏提供 Embedding 模型和回答生成模型切换按钮

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
