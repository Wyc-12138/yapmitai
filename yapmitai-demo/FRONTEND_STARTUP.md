# 前端启动文档

## 1. 环境要求

- Windows 10/11
- Node.js 版本必须大于 22（推荐 Node.js 24 LTS）
- 后端默认运行在 `http://localhost:8000`

检查 Node.js：

```powershell
node --version
npm --version
```

## 2. 进入前端目录

```powershell
cd F:\code\YP\yapmitai-demo
```

## 3. 启动前端

首次启动先安装 Vue 3、Vue Router 和 Vite 依赖：

```powershell
npm.cmd install
```

然后启动 Vite 开发服务器：

```powershell
npm.cmd run dev
```

看到 Vite 输出本地地址表示启动成功：

```text
Local: http://localhost:5173/
```

浏览器访问：

```text
http://localhost:5173
```

模型配置页面：

```text
http://localhost:5173/enterprise/model-configs
```

企业智库页面：

```text
http://localhost:5173/enterprise/knowledge/agent
```

## 4. 前后端联调

前端接口文件默认请求：

```text
http://localhost:8000/api/v1
```

请求头使用：

```text
X-API-Key: yap_demo_key_2026
```

后端 `.env` 中应允许前端地址：

```env
CORS_ORIGINS=http://localhost:5173
```

## 5. 更换前端端口

PowerShell：

```powershell
$env:PORT=5174
npm.cmd run dev
```

更换端口后，需要同步修改后端 `.env` 的 `CORS_ORIGINS`。

## 6. 构建检查

```powershell
npm.cmd run build
```

该命令会使用 Vite 编译 Vue 3 应用，并生成 `dist` 生产目录。

构建完成后可执行：

```powershell
npm.cmd run preview
```

## 7. 常见问题

### 端口被占用

```powershell
Get-NetTCPConnection -LocalPort 5173 -State Listen
```

关闭对应进程或使用其他端口启动。

### 页面能打开但数据加载失败

依次检查：

1. 后端是否运行在 `http://localhost:8000`。
2. `http://localhost:8000/health` 是否返回成功。
3. PostgreSQL 是否已启动。
4. 浏览器控制台是否出现 CORS 或 API Key 错误。

### 停止前端

在启动前端的控制台按 `Ctrl+C`。
