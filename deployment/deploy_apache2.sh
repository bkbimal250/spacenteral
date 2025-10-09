#!/bin/bash

# SpaCentral Apache2 Production Deployment Script
# Run this script on your Apache2 production server

set -e  # Exit on error

echo "🚀 Starting SpaCentral Apache2 Deployment..."

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

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: Please run as root or with sudo${NC}"
    exit 1
fi

# Navigate to project directory
echo -e "${GREEN}📂 Navigating to project directory...${NC}"
cd $PROJECT_DIR || exit 1

# Pull latest code (if using git)
echo -e "${GREEN}📥 Pulling latest code...${NC}"
# git pull origin main  # Uncomment if using git

# Set proper ownership
echo -e "${GREEN}👤 Setting proper ownership...${NC}"
chown -R www-data:www-data $PROJECT_DIR

# Activate virtual environment
echo -e "${GREEN}🔧 Activating virtual environment...${NC}"
source $VENV_DIR/bin/activate

# Install/Update dependencies
echo -e "${GREEN}📦 Installing dependencies...${NC}"
$PIP install -r requirements.txt --upgrade

# Collect static files
echo -e "${GREEN}📁 Collecting static files...${NC}"
sudo -u www-data $PYTHON manage.py collectstatic --noinput

# Run migrations
echo -e "${GREEN}🗃️  Running database migrations...${NC}"
sudo -u www-data $PYTHON manage.py migrate --noinput

# Create logs directory if not exists
echo -e "${GREEN}📝 Creating logs directory...${NC}"
mkdir -p $PROJECT_DIR/logs
chown -R www-data:www-data $PROJECT_DIR/logs
chmod -R 775 $PROJECT_DIR/logs

# Set proper permissions
echo -e "${GREEN}🔐 Setting proper permissions...${NC}"
find $PROJECT_DIR -type d -exec chmod 755 {} \;
find $PROJECT_DIR -type f -exec chmod 644 {} \;
chmod -R 775 $PROJECT_DIR/media
chmod -R 775 $PROJECT_DIR/logs

# Check Django deployment configuration
echo -e "${GREEN}✅ Checking deployment configuration...${NC}"
$PYTHON manage.py check --deploy || echo -e "${YELLOW}⚠️  Some deployment checks failed. Review above warnings.${NC}"

# Restart services
echo -e "${GREEN}🔄 Restarting services...${NC}"

# Restart Daphne (WebSocket server)
if systemctl is-active --quiet daphne; then
    systemctl restart daphne
    echo -e "${GREEN}✅ Daphne service restarted${NC}"
else
    echo -e "${YELLOW}⚠️  Daphne service not running. Starting...${NC}"
    systemctl start daphne
fi

# Reload Apache
if systemctl is-active --quiet apache2; then
    # Test Apache configuration first
    if apache2ctl configtest; then
        systemctl reload apache2
        echo -e "${GREEN}✅ Apache2 reloaded${NC}"
    else
        echo -e "${RED}❌ Apache configuration test failed. Not reloading.${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Apache2 is not running!${NC}"
    exit 1
fi

# Check service status
echo -e "\n${GREEN}📊 Service Status:${NC}"
echo -e "\n${YELLOW}Apache2:${NC}"
systemctl status apache2 --no-pager -l | head -n 20

echo -e "\n${YELLOW}Daphne (WebSocket):${NC}"
systemctl status daphne --no-pager -l | head -n 20

echo -e "\n${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Application should be running at your domain${NC}"

# Show recent logs
echo -e "\n${YELLOW}📝 Recent Django logs:${NC}"
if [ -f "$PROJECT_DIR/logs/django.log" ]; then
    tail -n 20 $PROJECT_DIR/logs/django.log
else
    echo -e "${YELLOW}No Django logs found yet.${NC}"
fi

echo -e "\n${YELLOW}📝 Recent Apache error logs:${NC}"
tail -n 20 /var/log/apache2/spacentral-error.log 2>/dev/null || tail -n 20 /var/log/apache2/error.log

echo -e "\n${GREEN}💡 Useful commands:${NC}"
echo "  - View Django logs: tail -f $PROJECT_DIR/logs/django.log"
echo "  - View Apache logs: tail -f /var/log/apache2/spacentral-error.log"
echo "  - View Daphne logs: journalctl -u daphne -f"
echo "  - Restart Apache: systemctl restart apache2"
echo "  - Restart Daphne: systemctl restart daphne"
echo "  - Check Apache config: apache2ctl configtest"
echo "  - Django shell: $PYTHON manage.py shell"
echo "  - Apache status: systemctl status apache2"

echo -e "\n${GREEN}🎉 All done!${NC}"

