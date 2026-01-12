#!/bin/bash

# PayCoreX Deployment Setup Script
# This script sets up systemd services, nginx, and enables auto-start

set -e

PROJECT_DIR="/home/ubuntu/PayCoreX"
SERVICE_DIR="/etc/systemd/system"
NGINX_DIR="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

echo "=== PayCoreX Deployment Setup ==="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./setup-deployment.sh"
    exit 1
fi

# Create logs directory
echo "Creating logs directory..."
mkdir -p $PROJECT_DIR/logs
chown ubuntu:ubuntu $PROJECT_DIR/logs

# Copy systemd service files
echo "Installing systemd service files..."
cp $PROJECT_DIR/paycorex-gunicorn.service $SERVICE_DIR/
cp $PROJECT_DIR/paycorex-celery.service $SERVICE_DIR/

# Copy nginx configuration
echo "Installing Nginx configuration..."
cp $PROJECT_DIR/paycorex-nginx.conf $NGINX_DIR/paycorex

# Create symlink for nginx (remove default if exists)
if [ -L "$NGINX_ENABLED/default" ]; then
    echo "Removing default Nginx site..."
    rm $NGINX_ENABLED/default
fi

# Create symlink for paycorex
if [ ! -L "$NGINX_ENABLED/paycorex" ]; then
    ln -s $NGINX_DIR/paycorex $NGINX_ENABLED/paycorex
fi

# Reload systemd
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable services to start on boot
echo "Enabling services to start on boot..."
systemctl enable paycorex-gunicorn
systemctl enable paycorex-celery

# Test nginx configuration
echo "Testing Nginx configuration..."
nginx -t

# Create staticfiles directory
echo "Creating staticfiles directory..."
mkdir -p $PROJECT_DIR/staticfiles
chown ubuntu:ubuntu $PROJECT_DIR/staticfiles

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Make sure PostgreSQL and Redis are installed and running:"
echo "   sudo systemctl status postgresql"
echo "   sudo systemctl status redis"
echo ""
echo "2. Create the database if it doesn't exist:"
echo "   sudo -u postgres psql -c 'CREATE DATABASE paycorex;'"
echo ""
echo "3. Install Python dependencies:"
echo "   cd $PROJECT_DIR"
echo "   python3 -m pip install -r requirements.txt"
echo ""
echo "4. Run migrations:"
echo "   cd $PROJECT_DIR"
echo "   python3 manage.py migrate"
echo ""
echo "5. Collect static files:"
echo "   python3 manage.py collectstatic --noinput"
echo ""
echo "6. Start services:"
echo "   cd $PROJECT_DIR"
echo "   ./manage-services.sh start"
echo ""
echo "7. Check status:"
echo "   ./manage-services.sh status"
echo ""


