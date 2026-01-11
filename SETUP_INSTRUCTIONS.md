# PayCoreX Setup Instructions

## Environment Configuration Complete ✓

Your `.env` file is configured with all required variables.

## Next Steps

### 1. Update Database Password

The default password in `.env` is `postgres`. Update it if your PostgreSQL uses a different password:

**Option A: Edit .env manually**
- Open `.env` file
- Change `DB_PASSWORD=postgres` to your actual PostgreSQL password

**Option B: Use PowerShell script**
```powershell
.\update_db_password.ps1 -Password "your_actual_password"
```

### 2. Ensure Services Are Running

**PostgreSQL:**
- Ensure PostgreSQL is installed and running
- Default: `localhost:5432`
- Create database if it doesn't exist:
  ```sql
  CREATE DATABASE paycorex;
  ```

**Redis:**
- Ensure Redis is installed and running
- Default: `localhost:6379`
- Windows: Download from https://github.com/microsoftarchive/redis/releases
- Or use Docker: `docker run -d -p 6379:6379 redis`

### 3. Run Database Migrations

```bash
python manage.py migrate
```

This will create all database tables.

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

Server will run on `http://127.0.0.1:8000/`

### 6. Start Celery Worker (Optional - for background tasks)

Open a new terminal:
```bash
celery -A core worker -l info
```

## Verify Setup

Run the configuration check:
```bash
python check_setup.py
```

## Test API

Once server is running, test the merchant registration:
```bash
curl -X POST http://127.0.0.1:8000/v1/merchants/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Merchant", "email": "test@example.com"}'
```

## Troubleshooting

**Database Connection Error:**
- Verify PostgreSQL is running: `pg_isready` or check Windows Services
- Verify password in `.env` matches PostgreSQL password
- Verify database `paycorex` exists

**Redis Connection Error:**
- Verify Redis is running: `redis-cli ping` (should return PONG)
- Check Redis URL in `.env`

**Migration Errors:**
- Ensure database exists
- Check database user has CREATE privileges

