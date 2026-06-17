#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:?Usage: sudo bash deploy/deploy_server.sh your-domain.com admin@example.com}"
EMAIL="${2:?Usage: sudo bash deploy/deploy_server.sh your-domain.com admin@example.com}"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_DIR="$APP_DIR/deploy"
WEB_ROOT="/var/www/yapmitai/dist"

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root: sudo bash deploy/deploy_server.sh $DOMAIN $EMAIL"
  exit 1
fi

echo "[1/7] Installing system packages"
apt-get update
apt-get install -y ca-certificates curl gnupg nginx certbot python3-certbot-nginx rsync openssl

if ! command -v docker >/dev/null 2>&1; then
  echo "[2/7] Installing Docker"
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  . /etc/os-release
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" > /etc/apt/sources.list.d/docker.list
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
  echo "[2/7] Docker already installed"
fi

if ! command -v node >/dev/null 2>&1 || ! node -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 23 ? 0 : 1)' >/dev/null 2>&1; then
  echo "[3/7] Installing Node.js 24"
  curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
  apt-get install -y nodejs
else
  echo "[3/7] Node.js is new enough"
fi

echo "[4/7] Preparing backend environment"
if [ ! -f "$DEPLOY_DIR/.env.backend" ]; then
  cp "$DEPLOY_DIR/.env.backend.example" "$DEPLOY_DIR/.env.backend"
  API_KEY="$(openssl rand -hex 24)"
  MYSQL_ROOT_PASSWORD="$(openssl rand -hex 24)"
  MYSQL_PASSWORD="$(openssl rand -hex 24)"
  sed -i "s|change-this-api-key|$API_KEY|g" "$DEPLOY_DIR/.env.backend"
  sed -i "s|change-this-db-password|$MYSQL_PASSWORD|g" "$DEPLOY_DIR/.env.backend"
  sed -i "s|https://example.com|https://$DOMAIN|g" "$DEPLOY_DIR/.env.backend"
  {
    echo "MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD"
    echo "MYSQL_PASSWORD=$MYSQL_PASSWORD"
  } >> "$DEPLOY_DIR/.env.backend"
  echo "Created $DEPLOY_DIR/.env.backend. Add external AI keys there if needed."
fi

set -a
source "$DEPLOY_DIR/.env.backend"
set +a

echo "[5/7] Building and starting backend containers"
docker compose --env-file "$DEPLOY_DIR/.env.backend" -f "$DEPLOY_DIR/docker-compose.prod.yml" up -d --build

echo "[6/7] Building frontend"
cd "$APP_DIR/yapmitai-demo"
npm install
VITE_API_BASE_URL="/api/v1" VITE_API_KEY="$API_KEY" npm run build
mkdir -p "$WEB_ROOT"
rsync -a --delete dist/ "$WEB_ROOT/"
chown -R www-data:www-data /var/www/yapmitai

echo "[7/7] Configuring Nginx and HTTPS"
sed "s|__DOMAIN__|$DOMAIN|g" "$DEPLOY_DIR/nginx-yapmitai.conf.template" > /etc/nginx/sites-available/yapmitai
ln -sf /etc/nginx/sites-available/yapmitai /etc/nginx/sites-enabled/yapmitai
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" --redirect

echo "Done."
echo "Frontend: https://$DOMAIN"
echo "Backend health: https://$DOMAIN/health"
