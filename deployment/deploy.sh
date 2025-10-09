#!/bin/bash

# SpaCentral Production Deployment Script
# Run this script on your production server

set -e  # Exit on error

echo "🚀 Starting SpaCentral Deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/spacentral"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

# Check if running as root (for system services)
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Warning: Not running as root. Some operations may fail.${NC}"
fi

# Navigate to project directory
cd $PROJECT_DIR || exit 1

# Pull latest code (if using git)
echo -e "${GREEN}📥 Pulling latest code...${NC}"
# git pull origin main  # Uncomment if using git

# Activate virtual environment
echo -e "${GREEN}🔧 Activating virtual environment...${NC}"
source $VENV_DIR/bin/activate

# Install/Update dependencies
echo -e "${GREEN}📦 Installing dependencies...${NC}"
$PIP install -r requirements.txt --upgrade

# Collect static files
echo -e "${GREEN}📁 Collecting static files...${NC}"
$PYTHON manage.py collectstatic --noinput

# Run migrations
echo -e "${GREEN}🗃️  Running database migrations...${NC}"
$PYTHON manage.py migrate --noinput

# Create logs directory if not exists
mkdir -p $PROJECT_DIR/logs

# Check Django deployment configuration
echo -e "${GREEN}✅ Checking deployment configuration...${NC}"
$PYTHON manage.py check --deploy

# Restart services
echo -e "${GREEN}🔄 Restarting services...${NC}"

if systemctl is-active --quiet spacentral; then
    systemctl restart spacentral
    echo -e "${GREEN}✅ SpaCentral service restarted${NC}"
else
    echo -e "${YELLOW}⚠️  SpaCentral service not running. Starting...${NC}"
    systemctl start spacentral
fi

if systemctl is-active --quiet nginx; then
    systemctl reload nginx
    echo -e "${GREEN}✅ Nginx reloaded${NC}"
fi

# Check service status
echo -e "${GREEN}📊 Service Status:${NC}"
systemctl status spacentral --no-pager -l
systemctl status nginx --no-pager -l

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Application should be running at your domain${NC}"

# Show logs
echo -e "\n${YELLOW}📝 Recent logs:${NC}"
tail -n 20 $PROJECT_DIR/logs/django.log

echo -e "\n${GREEN}💡 Useful commands:${NC}"
echo "  - View logs: tail -f $PROJECT_DIR/logs/django.log"
echo "  - Restart app: systemctl restart spacentral"
echo "  - Check status: systemctl status spacentral"
echo "  - Django shell: $PYTHON manage.py shell"

