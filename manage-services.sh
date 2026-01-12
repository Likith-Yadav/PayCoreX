#!/bin/bash

# PayCoreX Service Management Script
# Usage: ./manage-services.sh [start|stop|restart|status]

SERVICES=("paycorex-gunicorn" "paycorex-celery")
NGINX_SERVICE="nginx"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if service is active
check_service() {
    systemctl is-active --quiet $1
}

# Function to check if service is enabled
check_enabled() {
    systemctl is-enabled --quiet $1
}

# Function to start services
start_services() {
    echo -e "${GREEN}Starting PayCoreX services...${NC}"
    
    # Create logs directory if it doesn't exist
    mkdir -p /home/ubuntu/PayCoreX/logs
    
    # Start PostgreSQL if not running
    if ! check_service postgresql; then
        echo -e "${YELLOW}Starting PostgreSQL...${NC}"
        sudo systemctl start postgresql
    fi
    
    # Start Redis if not running
    if ! check_service redis; then
        echo -e "${YELLOW}Starting Redis...${NC}"
        sudo systemctl start redis
    fi
    
    # Start application services
    for service in "${SERVICES[@]}"; do
        if check_service $service; then
            echo -e "${YELLOW}$service is already running${NC}"
        else
            echo -e "${GREEN}Starting $service...${NC}"
            sudo systemctl start $service
            sleep 2
        fi
    done
    
    # Start/Reload Nginx
    if check_service $NGINX_SERVICE; then
        echo -e "${YELLOW}Reloading Nginx...${NC}"
        sudo systemctl reload $NGINX_SERVICE
    else
        echo -e "${GREEN}Starting Nginx...${NC}"
        sudo systemctl start $NGINX_SERVICE
    fi
    
    echo -e "${GREEN}All services started!${NC}"
    status_services
}

# Function to stop services
stop_services() {
    echo -e "${RED}Stopping PayCoreX services...${NC}"
    
    # Stop Nginx
    if check_service $NGINX_SERVICE; then
        echo -e "${RED}Stopping Nginx...${NC}"
        sudo systemctl stop $NGINX_SERVICE
    fi
    
    # Stop application services
    for service in "${SERVICES[@]}"; do
        if check_service $service; then
            echo -e "${RED}Stopping $service...${NC}"
            sudo systemctl stop $service
        else
            echo -e "${YELLOW}$service is not running${NC}"
        fi
    done
    
    echo -e "${GREEN}All services stopped!${NC}"
}

# Function to restart services
restart_services() {
    echo -e "${YELLOW}Restarting PayCoreX services...${NC}"
    stop_services
    sleep 2
    start_services
}

# Function to show status
status_services() {
    echo -e "\n${GREEN}=== PayCoreX Service Status ===${NC}\n"
    
    # Check PostgreSQL
    if check_service postgresql; then
        echo -e "PostgreSQL: ${GREEN}● Running${NC}"
    else
        echo -e "PostgreSQL: ${RED}● Stopped${NC}"
    fi
    
    # Check Redis
    if check_service redis; then
        echo -e "Redis:      ${GREEN}● Running${NC}"
    else
        echo -e "Redis:      ${RED}● Stopped${NC}"
    fi
    
    # Check application services
    for service in "${SERVICES[@]}"; do
        if check_service $service; then
            enabled_status=""
            if check_enabled $service; then
                enabled_status=" (enabled)"
            fi
            echo -e "$service: ${GREEN}● Running${enabled_status}${NC}"
        else
            echo -e "$service: ${RED}● Stopped${NC}"
        fi
    done
    
    # Check Nginx
    if check_service $NGINX_SERVICE; then
        echo -e "Nginx:      ${GREEN}● Running${NC}"
    else
        echo -e "Nginx:      ${RED}● Stopped${NC}"
    fi
    
    echo ""
    
    # Show recent logs
    echo -e "${YELLOW}=== Recent Gunicorn Logs ===${NC}"
    if [ -f /home/ubuntu/PayCoreX/logs/gunicorn-error.log ]; then
        tail -n 5 /home/ubuntu/PayCoreX/logs/gunicorn-error.log
    else
        echo "No logs found"
    fi
    
    echo ""
}

# Main script logic
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        status_services
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start all PayCoreX services"
        echo "  stop    - Stop all PayCoreX services"
        echo "  restart - Restart all PayCoreX services"
        echo "  status  - Show status of all services"
        exit 1
        ;;
esac

exit 0


