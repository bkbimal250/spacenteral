# SpaCentral Apache2 Production Deployment Guide

## 🚀 Apache2 Production Setup

### Prerequisites

```bash
# Install required packages
sudo apt-get update
sudo apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-pip python3-venv mysql-client git
```

### 1. Enable Required Apache Modules

```bash
# Enable necessary Apache modules
sudo a2enmod wsgi
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
sudo a2enmod deflate
sudo a2enmod expires

# Restart Apache to apply changes
sudo systemctl restart apache2
```

### 2. Setup Project Directory

```bash
# Create project directory
sudo mkdir -p /var/www/spacentral
cd /var/www/spacentral

# Clone or copy your project files here
# git clone your-repo-url .

# Set proper permissions
sudo chown -R www-data:www-data /var/www/spacentral
sudo chmod -R 755 /var/www/spacentral
```

### 3. Create Python Virtual Environment

```bash
# Create virtual environment
cd /var/www/spacentral
sudo -u www-data python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate
deactivate
```

### 4. Configure Environment Variables

Create `.env` file in `/var/www/spacentral/.env`:

```bash
sudo nano /var/www/spacentral/.env
```

Add the following content:

```env
# Django Settings
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,82.25.109.137

# Database Configuration (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security Settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### 5. Setup Database and Static Files

```bash
cd /var/www/spacentral

# Run as www-data user
sudo -u www-data venv/bin/python manage.py migrate
sudo -u www-data venv/bin/python manage.py collectstatic --noinput
sudo -u www-data venv/bin/python manage.py createsuperuser

# Create logs directory
sudo mkdir -p /var/www/spacentral/logs
sudo chown -R www-data:www-data /var/www/spacentral/logs
```

### 6. Configure Apache VirtualHost

```bash
# Copy Apache configuration
sudo cp deployment/apache2.conf /etc/apache2/sites-available/spacentral.conf

# Edit the configuration file
sudo nano /etc/apache2/sites-available/spacentral.conf

# Update ServerName and ServerAlias with your domain
# Update file paths if different

# Disable default site and enable spacentral
sudo a2dissite 000-default.conf
sudo a2ensite spacentral.conf

# Test Apache configuration
sudo apache2ctl configtest

# If OK, reload Apache
sudo systemctl reload apache2
```

### 7. Setup WebSocket Support (Daphne)

```bash
# Copy Daphne service file
sudo cp deployment/daphne.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start Daphne service
sudo systemctl enable daphne
sudo systemctl start daphne

# Check status
sudo systemctl status daphne
```

### 8. Build and Deploy Frontend

```bash
# On your development machine or build server
cd frontend/Dashboard/admindashbboard

# Update API base URL in frontend code
# Edit src/services/api.js and set:
# const API_BASE_URL = 'https://yourdomain.com/api';

# Build frontend
npm run build

# Copy dist folder to server
scp -r dist/* user@yourserver:/var/www/spacentral/frontend/dist/

# Or if already on server
cd /var/www/spacentral/frontend/Dashboard/admindashbboard
npm install
npm run build
sudo cp -r dist/* /var/www/spacentral/frontend/dist/
```

### 9. Set Proper Permissions

```bash
# Set ownership
sudo chown -R www-data:www-data /var/www/spacentral

# Set directory permissions
sudo find /var/www/spacentral -type d -exec chmod 755 {} \;

# Set file permissions
sudo find /var/www/spacentral -type f -exec chmod 644 {} \;

# Make scripts executable
sudo chmod +x deployment/*.sh

# Special permissions for media and logs
sudo chmod -R 775 /var/www/spacentral/media
sudo chmod -R 775 /var/www/spacentral/logs
```

### 10. SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-apache

# Obtain SSL certificate
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

# Certbot will automatically configure Apache for HTTPS
# Follow the prompts

# Test auto-renewal
sudo certbot renew --dry-run
```

### 11. Configure Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Apache Full'
sudo ufw allow 22/tcp
sudo ufw enable

# Check status
sudo ufw status
```

### 12. Restart All Services

```bash
# Restart Apache
sudo systemctl restart apache2

# Restart Daphne (WebSocket)
sudo systemctl restart daphne

# Check status
sudo systemctl status apache2
sudo systemctl status daphne
```

## 📊 Monitoring and Maintenance

### View Logs

```bash
# Apache error log
sudo tail -f /var/log/apache2/spacentral-error.log

# Apache access log
sudo tail -f /var/log/apache2/spacentral-access.log

# Django application log
sudo tail -f /var/www/spacentral/logs/django.log

# Daphne service log
sudo journalctl -u daphne -f
```

### Common Commands

```bash
# Check Apache status
sudo systemctl status apache2

# Restart Apache
sudo systemctl restart apache2

# Reload Apache (without dropping connections)
sudo systemctl reload apache2

# Test Apache configuration
sudo apache2ctl configtest

# Check Apache modules
apache2ctl -M

# Restart Daphne
sudo systemctl restart daphne

# Check Daphne status
sudo systemctl status daphne
```

### Database Backup

```bash
# Create backup
mysqldump -h 82.25.109.137 -u dosadmin -p spacentraldata > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
mysql -h 82.25.109.137 -u dosadmin -p spacentraldata < backup_YYYYMMDD_HHMMSS.sql
```

### Update Deployment

```bash
# Run the deployment script
cd /var/www/spacentral
sudo bash deployment/deploy_apache2.sh
```

## 🔧 Troubleshooting

### Apache won't start
```bash
# Check configuration
sudo apache2ctl configtest

# Check error logs
sudo tail -f /var/log/apache2/error.log

# Check if port 80/443 is in use
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
```

### 500 Internal Server Error
```bash
# Check Apache error log
sudo tail -f /var/log/apache2/spacentral-error.log

# Check Django log
sudo tail -f /var/www/spacentral/logs/django.log

# Check permissions
ls -la /var/www/spacentral/
```

### Static files not loading
```bash
# Collect static files again
cd /var/www/spacentral
sudo -u www-data venv/bin/python manage.py collectstatic --noinput

# Check static files directory
ls -la /var/www/spacentral/staticfiles/

# Check Apache configuration for Alias directive
```

### WebSocket connection fails
```bash
# Check if Daphne is running
sudo systemctl status daphne

# Check Daphne logs
sudo journalctl -u daphne -n 50

# Test WebSocket connection
wscat -c ws://localhost:8001/ws/chat/test/
```

### Permission denied errors
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/spacentral

# Fix permissions
sudo chmod -R 755 /var/www/spacentral
sudo chmod -R 775 /var/www/spacentral/media
sudo chmod -R 775 /var/www/spacentral/logs
```

## 🎯 Performance Optimization

### Apache MPM Settings

Edit `/etc/apache2/mods-available/mpm_event.conf`:

```apache
<IfModule mpm_event_module>
    StartServers             2
    MinSpareThreads         25
    MaxSpareThreads         75
    ThreadLimit             64
    ThreadsPerChild         25
    MaxRequestWorkers      150
    MaxConnectionsPerChild   0
</IfModule>
```

### Enable Caching

```bash
# Enable mod_cache
sudo a2enmod cache
sudo a2enmod cache_disk

# Add to VirtualHost configuration
# CacheQuickHandler off
# CacheLock on
# CacheRoot /var/cache/apache2/mod_cache_disk
# CacheEnable disk /
# CacheIgnoreHeaders Set-Cookie
```

### Monitor Performance

```bash
# Apache server status (enable mod_status)
sudo a2enmod status

# Add to Apache config:
# <Location "/server-status">
#     SetHandler server-status
#     Require local
# </Location>

# View status
curl http://localhost/server-status
```

## 📋 Production Checklist

- [x] Apache2 installed and configured
- [x] MySQL database configured
- [x] All Python dependencies installed
- [x] Migrations applied
- [x] Static files collected
- [x] Media folder permissions set
- [x] Logs directory created
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] Firewall configured
- [x] Daphne service running
- [ ] Backup system configured
- [ ] Monitoring setup

## 🌐 Access Your Application

- **Frontend:** http://yourdomain.com or https://yourdomain.com
- **Admin Panel:** http://yourdomain.com/admin or https://yourdomain.com/admin
- **API:** http://yourdomain.com/api or https://yourdomain.com/api

## 📞 Support

**Database:** spacentraldata @ 82.25.109.137:3306
**Web Server:** Apache2 with mod_wsgi
**WebSocket:** Daphne on port 8001
**Status:** ✅ Production Ready with Apache2

For issues, check logs first:
- Apache: `/var/log/apache2/spacentral-error.log`
- Django: `/var/www/spacentral/logs/django.log`
- Daphne: `journalctl -u daphne -f`

