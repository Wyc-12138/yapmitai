# YAPMITAI 前后端服务器部署说明

本文档记录 YAPMITAI 项目在 Ubuntu 服务器上的部署流程，包含 Vue 前端、FastAPI 后端、MySQL、Nginx 反向代理和 HTTPS 配置。

## 适用范围

本文档适用于以下部署场景：

- 前端使用 Vue / Vite 打包为静态文件。
- 后端使用 FastAPI / Uvicorn 运行在服务器本机 `127.0.0.1:8000`。
- 数据库使用 MySQL。
- Web 入口使用 Nginx，负责前端静态资源和后端 API 反向代理。
- 域名使用 `yapmitai.com` 和 `www.yapmitai.com`。

## 部署结果

部署完成后，预期结果如下：

- `https://yapmitai.com` 可访问前端页面。
- `https://yapmitai.com/enterprise/tools` 可访问 AI 工具中心。
- `https://yapmitai.com/docs` 可访问 FastAPI Swagger 文档。
- 前端生产包请求 `/api/v1/...`，由 Nginx 转发到 FastAPI 后端。
- Nginx、MySQL、FastAPI 后端服务均可开机自启。

> 安全提示：本文档中的数据库密码和 API Key 为示例值。正式部署时建议替换为强密码，并避免将 `.env`、数据库密码、API Key 上传到 GitHub。

---

## 1. 部署环境

服务器系统：

```bash
Ubuntu
```

服务器公网 IP：

```text
47.238.147.245
```

域名：

```text
yapmitai.com
www.yapmitai.com
```

项目部署目录：

```text
/opt/yapmitai/
├── frontend-dist/   # Vue 前端打包后的静态文件
└── backend/         # FastAPI 后端项目
```

前端技术栈：

```text
Vue / Vite
```

后端技术栈：

```text
FastAPI / Uvicorn / Python 3.11
```

数据库：

```text
MySQL
```

Web 服务：

```text
Nginx
```

---

## 2. 阿里云防火墙配置

在阿里云轻量应用服务器控制台中，开放以下端口：

| 端口 | 协议 | 用途 |
|---|---|---|
| 22 | TCP | SSH 远程连接 |
| 80 | TCP | HTTP 访问 |
| 443 | TCP | HTTPS 访问 |

部署完成后，建议将 22 端口来源 IP 从 `0.0.0.0/0` 改为自己的公网 IP，提高安全性。

---

## 3. 域名解析配置

在阿里云控制台中添加域名解析：

| 主机记录 | 类型 | 记录值 |
|---|---|---|
| @ | A | 47.238.147.245 |
| www | A | 47.238.147.245 |

解析完成后，可以通过以下域名访问：

```text
http://yapmitai.com
http://www.yapmitai.com
```

---

## 4. 创建服务器项目目录

登录服务器后执行：

```bash
sudo mkdir -p /opt/yapmitai/frontend-dist
sudo mkdir -p /opt/yapmitai/backend
sudo chown -R $USER:$USER /opt/yapmitai
```

目录说明：

```text
/opt/yapmitai/frontend-dist  用于存放 Vue 打包后的 dist 内容
/opt/yapmitai/backend        用于存放 FastAPI 后端代码
```

---

## 5. 安装基础环境

在服务器上安装 Nginx、Python、MySQL 等依赖：

```bash
sudo apt update
sudo apt install nginx mysql-server python3.11 python3.11-venv python3.11-dev build-essential libssl-dev libffi-dev -y
```

启动并设置 Nginx 开机自启：

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

启动并设置 MySQL 开机自启：

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

检查服务状态：

```bash
sudo systemctl status nginx --no-pager
sudo systemctl status mysql --no-pager
```

---

## 6. 前端部署

### 6.1 前端环境变量配置

前端项目根目录：

```text
F:\code\YP\yapmitai-demo
```

在项目根目录创建 `.env.development`：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_API_KEY=yap_demo_key_2026
```

在项目根目录创建 `.env.production`：

```env
VITE_API_BASE_URL=/api/v1
VITE_API_KEY=yap_demo_key_2026
```

前端 `src/apiConfig.js` 配置：

```js
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "/api/v1";

export const API_KEY =
  import.meta.env.VITE_API_KEY || "yap_demo_key_2026";
```

说明：

```text
npm run dev    使用 .env.development
npm run build  使用 .env.production
```

本地开发时，请求地址为：

```text
http://localhost:8000/api/v1
```

线上部署后，请求地址为：

```text
/api/v1
```

Nginx 会将 `/api/v1/...` 转发到 FastAPI 后端。

### 6.2 本地打包前端

在 Windows 本地执行：

```cmd
cd /d F:\code\YP\yapmitai-demo
npm install
npm run build
```

打包成功后会生成：

```text
F:\code\YP\yapmitai-demo\dist
```

确认打包结果中不再包含 `localhost:8000`：

```powershell
cd F:\code\YP\yapmitai-demo
Select-String -Path .\dist\assets\*.js -Pattern "localhost:8000","127.0.0.1:8000"
```

如果没有输出，说明生产包配置正确。

### 6.3 上传前端 dist 到服务器

在 Windows 本地执行：

```cmd
cd /d F:\code\YP\yapmitai-demo

ssh root@47.238.147.245 "rm -rf /opt/yapmitai/frontend-dist/*"

scp -r dist/* root@47.238.147.245:/opt/yapmitai/frontend-dist/
```

上传后，服务器目录应类似：

```text
/opt/yapmitai/frontend-dist/
├── index.html
├── assets/
└── favicon.ico
```

---

## 7. 后端部署

### 7.1 上传后端代码

本地后端项目目录：

```text
F:\code\YP\yapmitai-backend
```

上传到服务器：

```cmd
cd /d F:\code\YP\yapmitai-backend

tar --exclude=node_modules --exclude=.git --exclude=.env -czf ..\backend.tar.gz .

scp ..\backend.tar.gz root@47.238.147.245:/opt/yapmitai/backend.tar.gz
```

服务器执行：

```bash
cd /opt/yapmitai/backend
tar -xzf ../backend.tar.gz -C .
rm ../backend.tar.gz
```

### 7.2 创建 Python 3.11 虚拟环境

服务器执行：

```bash
cd /opt/yapmitai/backend

python3.11 -m venv .venv

source .venv/bin/activate

python -V
```

确认显示：

```text
Python 3.11.x
```

### 7.3 安装后端依赖

```bash
cd /opt/yapmitai/backend
source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install cryptography
```

说明：

```text
cryptography 用于兼容 MySQL 8 的 caching_sha2_password 认证方式。
```

建议将其加入 `requirements.txt`：

```bash
echo "cryptography" >> requirements.txt
```

---

## 8. MySQL 配置

### 8.1 创建数据库和用户

进入 MySQL：

```bash
sudo mysql
```

执行：

```sql
DROP USER IF EXISTS 'yapmitai'@'localhost';
DROP USER IF EXISTS 'yapmitai'@'127.0.0.1';

CREATE DATABASE IF NOT EXISTS yapmitai
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER 'yapmitai'@'localhost'
IDENTIFIED BY 'Yapmitai_2026_pwd';

CREATE USER 'yapmitai'@'127.0.0.1'
IDENTIFIED BY 'Yapmitai_2026_pwd';

GRANT ALL PRIVILEGES ON yapmitai.* TO 'yapmitai'@'localhost';
GRANT ALL PRIVILEGES ON yapmitai.* TO 'yapmitai'@'127.0.0.1';

FLUSH PRIVILEGES;

EXIT;
```

建议密码只使用字母、数字、下划线，避免在数据库连接 URL 中因为特殊字符导致解析问题。

### 8.2 测试 MySQL 用户

```bash
mysql -h 127.0.0.1 -u yapmitai -p
```

输入密码后执行：

```sql
SHOW DATABASES;
EXIT;
```

如果能正常进入并看到 `yapmitai` 数据库，说明数据库用户配置成功。

---

## 9. 后端环境变量配置

在服务器创建后端 `.env`：

```bash
cd /opt/yapmitai/backend
nano .env
```

示例内容：

```env
DATABASE_URL=mysql+aiomysql://yapmitai:Yapmitai_2026_pwd@127.0.0.1:3306/yapmitai
API_KEY=yap_demo_key_2026
NODE_ENV=production
```

如果项目使用分散的 MySQL 配置，也可以使用：

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=yapmitai
MYSQL_PASSWORD=Yapmitai_2026_pwd
MYSQL_DATABASE=yapmitai
API_KEY=yap_demo_key_2026
```

具体变量名以项目代码读取的环境变量为准。

---

## 10. 测试启动 FastAPI

服务器执行：

```bash
cd /opt/yapmitai/backend
source .venv/bin/activate

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

如果看到：

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

说明后端启动成功。

测试接口文档：

```bash
curl http://127.0.0.1:8000/docs
```

测试业务接口：

```bash
curl -H "X-API-Key: yap_demo_key_2026" http://127.0.0.1:8000/api/v1/tools
```

如果返回数据或空列表，说明后端接口正常。

测试完成后，按：

```text
Ctrl + C
```

停止临时运行。

---

## 11. 使用 systemd 托管后端服务

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/yapmitai-backend.service
```

写入：

```ini
[Unit]
Description=Yapmitai FastAPI Backend
After=network.target mysql.service

[Service]
User=admin
WorkingDirectory=/opt/yapmitai/backend
Environment="PATH=/opt/yapmitai/backend/.venv/bin"
EnvironmentFile=-/opt/yapmitai/backend/.env
ExecStart=/opt/yapmitai/backend/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

加载并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start yapmitai-backend
sudo systemctl enable yapmitai-backend
```

查看状态：

```bash
sudo systemctl status yapmitai-backend --no-pager
```

查看日志：

```bash
journalctl -u yapmitai-backend -f
```

如果状态为：

```text
active (running)
```

说明后端已经后台运行成功。

---

## 12. Nginx 配置前端和后端代理

创建或编辑 Nginx 配置：

```bash
sudo nano /etc/nginx/sites-available/yapmitai
```

写入：

```nginx
server {
    listen 80;
    server_name yapmitai.com www.yapmitai.com;

    root /opt/yapmitai/frontend-dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
        proxy_set_header Host $host;
    }
}
```

> 重要：`proxy_pass http://127.0.0.1:8000;` 中 `8000` 后面不要加 `/`。
>
> 前端请求 `/api/v1/tools` 时，Nginx 应转发到 `http://127.0.0.1:8000/api/v1/tools`。
>
> 如果写成 `proxy_pass http://127.0.0.1:8000/;`，Nginx 可能会把 `/api` 截掉，变成 `http://127.0.0.1:8000/v1/tools`，从而导致接口 404。

### 12.1 启用 Nginx 配置

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/yapmitai /etc/nginx/sites-enabled/yapmitai
sudo nginx -t
sudo systemctl reload nginx
```

---

## 13. 访问测试

### 13.1 测试前端

浏览器访问：

```text
http://yapmitai.com
```

或：

```text
http://yapmitai.com/enterprise/tools
```

如果页面正常显示，说明前端部署成功。

### 13.2 测试后端文档

浏览器访问：

```text
http://yapmitai.com/docs
```

如果能打开 Swagger UI，说明后端代理成功。

### 13.3 测试后端接口

服务器执行：

```bash
curl -H "X-API-Key: yap_demo_key_2026" http://yapmitai.com/api/v1/tools
```

如果返回数据或空列表，说明 Nginx 到 FastAPI 的代理正常。

---

## 14. 配置 HTTPS

确认 HTTP 正常后，安装 Certbot：

```bash
sudo apt install certbot python3-certbot-nginx -y
```

申请 SSL 证书：

```bash
sudo certbot --nginx -d yapmitai.com -d www.yapmitai.com
```

按提示完成配置。

完成后访问：

```text
https://yapmitai.com
https://yapmitai.com/docs
```

检查自动续期：

```bash
sudo certbot renew --dry-run
```

---

## 15. 更新前端流程

本地执行：

```cmd
cd /d F:\code\YP\yapmitai-demo
npm run build
```

确认生产包不含本地地址：

```powershell
Select-String -Path .\dist\assets\*.js -Pattern "localhost:8000","127.0.0.1:8000"
```

上传：

```cmd
ssh root@47.238.147.245 "rm -rf /opt/yapmitai/frontend-dist/*"
scp -r dist/* root@47.238.147.245:/opt/yapmitai/frontend-dist/
```

浏览器强制刷新：

```text
Ctrl + F5
```

---

## 16. 更新后端流程

本地打包后端：

```cmd
cd /d F:\code\YP\yapmitai-backend
tar --exclude=node_modules --exclude=.git --exclude=.env -czf ..\backend.tar.gz .
scp ..\backend.tar.gz root@47.238.147.245:/opt/yapmitai/backend.tar.gz
```

服务器更新：

```bash
cd /opt/yapmitai/backend
tar -xzf ../backend.tar.gz -C .
rm ../backend.tar.gz

source .venv/bin/activate
pip install -r requirements.txt

sudo systemctl restart yapmitai-backend
sudo systemctl status yapmitai-backend --no-pager
```

查看日志：

```bash
journalctl -u yapmitai-backend -f
```

---

## 17. 常用检查命令

检查 Nginx：

```bash
sudo nginx -t
sudo systemctl status nginx --no-pager
```

检查后端：

```bash
sudo systemctl status yapmitai-backend --no-pager
journalctl -u yapmitai-backend -f
```

检查 MySQL：

```bash
sudo systemctl status mysql --no-pager
```

检查端口：

```bash
sudo ss -lntp | grep -E "80|443|8000|3306"
```

测试后端本机接口：

```bash
curl http://127.0.0.1:8000/docs
curl -H "X-API-Key: yap_demo_key_2026" http://127.0.0.1:8000/api/v1/tools
```

测试域名接口：

```bash
curl -H "X-API-Key: yap_demo_key_2026" http://yapmitai.com/api/v1/tools
```

---

## 18. 常见问题排查

### 18.1 前端控制台出现 `localhost:8000`

原因：

```text
前端生产包中仍然使用了本地 API 地址。
```

解决：

确认 `.env.production` 内容：

```env
VITE_API_BASE_URL=/api/v1
VITE_API_KEY=yap_demo_key_2026
```

重新打包并上传：

```cmd
npm run build
scp -r dist/* root@47.238.147.245:/opt/yapmitai/frontend-dist/
```

### 18.2 接口返回 404

检查 Nginx `/api/` 配置：

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
}
```

注意 `8000` 后面不要加 `/`。

### 18.3 接口返回 401

错误示例：

```json
{"code":401,"msg":"Unauthorized: invalid X-API-Key"}
```

原因：

```text
请求头缺少 X-API-Key，或 API Key 不一致。
```

解决：

前端 `.env.production` 中配置：

```env
VITE_API_KEY=yap_demo_key_2026
```

后端 `.env` 中配置相同的 Key。

### 18.4 FastAPI 连接 MySQL 失败

检查 MySQL 是否启动：

```bash
sudo systemctl status mysql --no-pager
```

检查数据库用户能否登录：

```bash
mysql -h 127.0.0.1 -u yapmitai -p
```

检查 `.env` 中数据库连接配置：

```env
DATABASE_URL=mysql+aiomysql://yapmitai:Yapmitai_2026_pwd@127.0.0.1:3306/yapmitai
```

### 18.5 缺少 cryptography

错误示例：

```text
RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
```

解决：

```bash
cd /opt/yapmitai/backend
source .venv/bin/activate
pip install cryptography
```

---

## 19. 最终部署完成检查清单

确认以下地址均可访问：

```text
http://yapmitai.com
http://yapmitai.com/enterprise/tools
http://yapmitai.com/docs
https://yapmitai.com
https://yapmitai.com/docs
```

确认以下服务均为 running：

```bash
sudo systemctl status nginx --no-pager
sudo systemctl status mysql --no-pager
sudo systemctl status yapmitai-backend --no-pager
```

确认浏览器控制台中：

```text
不再出现 localhost:8000
不再出现 /api/v1/... 404
不再出现 X-API-Key 401
```

至此，YAPMITAI 前后端部署完成。
