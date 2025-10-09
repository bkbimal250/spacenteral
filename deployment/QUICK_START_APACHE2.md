# 🚀 SpaCentral Apache2 Quick Start Guide

## One-Command Deployment (After Initial Setup)

```bash
cd /var/www/spacentral && sudo bash deployment/deploy_apache2.sh
```

## Initial Setup Steps (First Time Only)

### 1. Install Apache2 and Dependencies

```bash
sudo apt-get update && sudo apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    python3-pip \
    python3-venv \
    mysql-client \
    git
```

### 2. Enable Apache Modules

```bash
sudo a2enmod wsgi rewrite headers ssl proxy proxy_http proxy_wstunnel deflate expires
sudo systemctl restart apache2
```

### 3. Setup Project

```bash
# Create directory
sudo mkdir -p /var/www/spacentral
cd /var/www/spacentral

# Copy/Clone your project here
# (Upload files or git clone)

# Create virtual environment
sudo -u www-data python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 4. Create .env File

```bash
sudo nano /var/www/spacentral/.env
```

Paste:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,*
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 5. Setup Database and Static Files

```bash
cd /var/www/spacentral
sudo -u www-data venv/bin/python manage.py migrate
sudo -u www-data venv/bin/python manage.py collectstatic --noinput
sudo -u www-data venv/bin/python manage.py createsuperuser
```

### 6. Configure Apache

```bash
# Copy configuration
sudo cp deployment/apache2.conf /etc/apache2/sites-available/spacentral.conf

# Edit to match your domain
sudo nano /etc/apache2/sites-available/spacentral.conf
# Update: ServerName yourdomain.com
#         ServerAlias www.yourdomain.com

# Enable site
sudo a2dissite 000-default.conf
sudo a2ensite spacentral.conf
sudo apache2ctl configtest
sudo systemctl reload apache2
```

### 7. Setup WebSocket Service

```bash
sudo cp deployment/daphne.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable daphne
sudo systemctl start daphne
```

### 8. Set Permissions

```bash
sudo chown -R www-data:www-data /var/www/spacentral
sudo chmod -R 755 /var/www/spacentral
sudo chmod -R 775 /var/www/spacentral/media
sudo chmod -R 775 /var/www/spacentral/logs
```

### 9. Setup SSL (Optional but Recommended)

```bash
sudo apt-get install certbot python3-certbot-apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

## ✅ Verification

```bash
# Check Apache
sudo systemctl status apache2

# Check Daphne
sudo systemctl status daphne

# Check logs
sudo tail -f /var/log/apache2/spacentral-error.log
sudo tail -f /var/www/spacentral/logs/django.log
```

## 🌐 Access

- **Frontend:** http://yourdomain.com
- **Admin:** http://yourdomain.com/admin
- **API:** http://yourdomain.com/api

## 🔧 Common Commands

```bash
# Restart Apache
sudo systemctl restart apache2

# Restart Daphne
sudo systemctl restart daphne

# View logs
sudo tail -f /var/log/apache2/spacentral-error.log
sudo tail -f /var/www/spacentral/logs/django.log
sudo journalctl -u daphne -f

# Collect static files
sudo -u www-data /var/www/spacentral/venv/bin/python /var/www/spacentral/manage.py collectstatic --noinput

# Run migrations
sudo -u www-data /var/www/spacentral/venv/bin/python /var/www/spacentral/manage.py migrate

# Django shell
sudo -u www-data /var/www/spacentral/venv/bin/python /var/www/spacentral/manage.py shell
```

## 🆘 Troubleshooting

### Apache won't start
```bash
sudo apache2ctl configtest
sudo tail -f /var/log/apache2/error.log
```

### 500 Error
```bash
sudo tail -f /var/log/apache2/spacentral-error.log
sudo tail -f /var/www/spacentral/logs/django.log
```

### Permission Issues
```bash
sudo chown -R www-data:www-data /var/www/spacentral
sudo chmod -R 755 /var/www/spacentral
```

### WebSocket Not Working
```bash
sudo systemctl restart daphne
sudo journalctl -u daphne -f
```

## 📊 Database Info

- **Host:** 82.25.109.137
- **Port:** 3306
- **Database:** spacentraldata
- **User:** dosadmin

## 🎉 Done!

Your SpaCentral application should now be running on Apache2!

