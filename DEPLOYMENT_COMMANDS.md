# PayCoreX Deployment Commands

This document contains all the commands you need to manage your PayCoreX backend on SSH.

## Quick Reference

### Service Management (Recommended)
```bash
cd /home/ubuntu/PayCoreX

# Start all services
./manage-services.sh start

# Stop all services
./manage-services.sh stop

# Restart all services
./manage-services.sh restart

# Check status of all services
./manage-services.sh status
```

### Individual Service Commands

#### Gunicorn (Django Backend)
```bash
# Start
sudo systemctl start paycorex-gunicorn

# Stop
sudo systemctl stop paycorex-gunicorn

# Restart
sudo systemctl restart paycorex-gunicorn

# Status
sudo systemctl status paycorex-gunicorn

# Enable auto-start on boot
sudo systemctl enable paycorex-gunicorn

# Disable auto-start
sudo systemctl disable paycorex-gunicorn

# View logs
sudo journalctl -u paycorex-gunicorn -f
# Or
tail -f /home/ubuntu/PayCoreX/logs/gunicorn-error.log
```

#### Celery Worker
```bash
# Start
sudo systemctl start paycorex-celery

# Stop
sudo systemctl stop paycorex-celery

# Restart
sudo systemctl restart paycorex-celery

# Status
sudo systemctl status paycorex-celery

# Enable auto-start on boot
sudo systemctl enable paycorex-celery

# View logs
sudo journalctl -u paycorex-celery -f
# Or
tail -f /home/ubuntu/PayCoreX/logs/celery-worker.log
```

#### Nginx
```bash
# Start
sudo systemctl start nginx

# Stop
sudo systemctl stop nginx

# Restart
sudo systemctl restart nginx

# Reload (without downtime)
sudo systemctl reload nginx

# Status
sudo systemctl status nginx

# Test configuration
sudo nginx -t

# View logs
sudo tail -f /var/log/nginx/paycorex-error.log
sudo tail -f /var/log/nginx/paycorex-access.log
```

#### PostgreSQL
```bash
# Start
sudo systemctl start postgresql

# Stop
sudo systemctl stop postgresql

# Restart
sudo systemctl restart postgresql

# Status
sudo systemctl status postgresql

# Enable auto-start
sudo systemctl enable postgresql

# Connect to database
sudo -u postgres psql
# Or connect to specific database
sudo -u postgres psql paycorex
```

#### Redis
```bash
# Start
sudo systemctl start redis

# Stop
sudo systemctl stop redis

# Restart
sudo systemctl restart redis

# Status
sudo systemctl status redis

# Enable auto-start
sudo systemctl enable redis

# Test connection
redis-cli ping
```

## Initial Setup

### 1. Install Dependencies
```bash
# Install system packages
sudo apt update
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib redis-server nginx

# Install Python packages
cd /home/ubuntu/PayCoreX
python3 -m pip install --user -r requirements.txt
# Or if using venv:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE paycorex;"

# Create user (if needed)
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "ALTER USER postgres CREATEDB;"

# Update .env file with correct database password
nano /home/ubuntu/PayCoreX/.env
```

### 3. Run Migrations
```bash
cd /home/ubuntu/PayCoreX
python3 manage.py migrate
python3 manage.py collectstatic --noinput
```

### 4. Setup Services
```bash
cd /home/ubuntu/PayCoreX
sudo ./setup-deployment.sh
```

### 5. Start Services
```bash
cd /home/ubuntu/PayCoreX
./manage-services.sh start
```

## Common Tasks

### View All Service Status
```bash
./manage-services.sh status
```

### Restart After Code Changes
```bash
./manage-services.sh restart
```

### View Application Logs
```bash
# Gunicorn logs
tail -f /home/ubuntu/PayCoreX/logs/gunicorn-error.log
tail -f /home/ubuntu/PayCoreX/logs/gunicorn-access.log

# Celery logs
tail -f /home/ubuntu/PayCoreX/logs/celery-worker.log

# Nginx logs
sudo tail -f /var/log/nginx/paycorex-error.log
sudo tail -f /var/log/nginx/paycorex-access.log
```

### Check if Services are Running
```bash
# Check all at once
systemctl is-active paycorex-gunicorn paycorex-celery nginx postgresql redis

# Check individually
systemctl is-active paycorex-gunicorn && echo "Gunicorn: Running" || echo "Gunicorn: Stopped"
systemctl is-active paycorex-celery && echo "Celery: Running" || echo "Celery: Stopped"
systemctl is-active nginx && echo "Nginx: Running" || echo "Nginx: Stopped"
systemctl is-active postgresql && echo "PostgreSQL: Running" || echo "PostgreSQL: Stopped"
systemctl is-active redis && echo "Redis: Running" || echo "Redis: Stopped"
```

### Enable Auto-Start on Boot
```bash
sudo systemctl enable paycorex-gunicorn
sudo systemctl enable paycorex-celery
sudo systemctl enable postgresql
sudo systemctl enable redis
sudo systemctl enable nginx
```

### Disable Auto-Start
```bash
sudo systemctl disable paycorex-gunicorn
sudo systemctl disable paycorex-celery
```

## Troubleshooting

### Service Won't Start
```bash
# Check service status
sudo systemctl status paycorex-gunicorn

# Check logs
sudo journalctl -u paycorex-gunicorn -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "SELECT version();"

# Check if database exists
sudo -u postgres psql -l | grep paycorex

# Test connection from Django
cd /home/ubuntu/PayCoreX
python3 manage.py dbshell
```

### Redis Connection Issues
```bash
# Test Redis
redis-cli ping

# Check Redis status
sudo systemctl status redis
```

### Nginx Issues
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Reload configuration
sudo systemctl reload nginx
```

## File Locations

- Project Directory: `/home/ubuntu/PayCoreX`
- Service Files: `/etc/systemd/system/paycorex-*.service`
- Nginx Config: `/etc/nginx/sites-available/paycorex`
- Logs: `/home/ubuntu/PayCoreX/logs/`
- Nginx Logs: `/var/log/nginx/paycorex-*.log`
- Environment File: `/home/ubuntu/PayCoreX/.env`

## Ports

- Nginx: `80` (HTTP)
- Gunicorn: `8000` (internal, proxied by Nginx)
- PostgreSQL: `5432`
- Redis: `6379`


