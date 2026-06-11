# MySQL setup

The backend now uses MySQL 8 with SQLAlchemy's asynchronous `aiomysql` driver.

## Local MySQL

Create a user with permission to create the `yapmitai` database, or use an
existing administrative account. Configure `.env`:

```env
DATABASE_URL=mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/yapmitai?charset=utf8mb4
```

The backend creates the `yapmitai` database automatically when the configured
user has `CREATE DATABASE` permission. It then creates missing tables and seeds
the default model, agent, and skill records.

If the account cannot create databases, create it manually:

```sql
CREATE DATABASE IF NOT EXISTS yapmitai
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

## Docker

```powershell
docker compose up --build
```

The compose stack starts MySQL 8.4, Redis, and the FastAPI service.

## Important

Existing PostgreSQL rows are not copied automatically. Chroma vectors and
uploaded files remain in `storage/chroma` and `storage/knowledge`, but their
MySQL metadata must be recreated or migrated separately.
