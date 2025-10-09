# SpaCentral Production Deployment Guide

## 🚀 Production Configuration

### 1. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-very-secure-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,82.25.109.137,*

# Database Configuration (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,http://localhost:5173

# Security Settings
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

### 2. Database Setup (Already Completed)

✅ MySQL database is configured and migrations are applied
- **Host:** 82.25.109.137:3306
- **Database:** spacentraldata
- **User:** dosadmin

### 3. Static Files Collection

```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Production Server

#### Option A: Using Gunicorn (Recommended)

```bash
# Install gunicorn (if not already installed)
pip install gunicorn

# Run with gunicorn
gunicorn spa_central.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

#### Option B: Using Daphne (For WebSocket support)

```bash
# Install daphne (already in requirements.txt)
pip install daphne

# Run with daphne
daphne -b 0.0.0.0 -p 8000 spa_central.asgi:application
```

### 6. Frontend Deployment

#### Build Frontend

```bash
cd frontend/Dashboard/admindashbboard
npm run build
```

The build output will be in `dist/` folder.

#### Update API Base URL

Update the API base URL in frontend configuration to point to your production backend:

```javascript
// In frontend/Dashboard/admindashbboard/src/services/api.js
const API_BASE_URL = 'https://your-backend-domain.com/api';
```

### 7. Nginx Configuration (Recommended)

Create `/etc/nginx/sites-available/spacentral`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 100M;

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin Panel
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static Files
    location /static/ {
        alias /var/www/spacentral/staticfiles/;
    }

    # Media Files
    location /media/ {
        alias /var/www/spacentral/media/;
    }

    # WebSocket for Chat
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend
    location / {
        root /var/www/spacentral/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/spacentral /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 8. Systemd Service (Linux)

Create `/etc/systemd/system/spacentral.service`:

```ini
[Unit]
Description=SpaCentral Django Application
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/spacentral
Environment="PATH=/var/www/spacentral/venv/bin"
ExecStart=/var/www/spacentral/venv/bin/gunicorn spa_central.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable spacentral
sudo systemctl start spacentral
sudo systemctl status spacentral
```

### 9. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 10. Security Checklist

- [x] DEBUG = False in production
- [x] Strong SECRET_KEY
- [x] MySQL database configured
- [x] ALLOWED_HOSTS configured
- [x] CORS properly configured
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured
- [ ] Regular backups scheduled
- [x] Logging configured
- [ ] Monitoring setup (optional)

### 11. Environment-Specific Settings

#### Development (.env)
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
SECURE_SSL_REDIRECT=False
```

#### Production (.env)
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
```

### 12. Maintenance Commands

```bash
# Check system status
python manage.py check --deploy

# Create database backup
mysqldump -h 82.25.109.137 -u dosadmin -p spacentraldata > backup_$(date +%Y%m%d).sql

# View logs
tail -f logs/django.log

# Restart service
sudo systemctl restart spacentral

# Reload nginx
sudo systemctl reload nginx
```

### 13. Performance Optimization

1. **Enable Redis for Caching** (Optional)
```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Use Redis for Channel Layers** (For better WebSocket performance)
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### 14. Monitoring & Logging

- Application logs: `logs/django.log`
- Nginx access logs: `/var/log/nginx/access.log`
- Nginx error logs: `/var/log/nginx/error.log`
- System logs: `journalctl -u spacentral -f`

### 15. Database Connection Pooling (Optional)

Install django-mysql:
```bash
pip install django-mysql
```

Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spacentraldata',
        'USER': 'dosadmin',
        'PASSWORD': 'DishaSolution@8989',
        'HOST': '82.25.109.137',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

## 🔥 Quick Deployment Steps

1. Clone repository
2. Create `.env` file with production settings
3. Install dependencies: `pip install -r requirements.txt`
4. Collect static files: `python manage.py collectstatic`
5. Create superuser: `python manage.py createsuperuser`
6. Run with Gunicorn: `gunicorn spa_central.wsgi:application --bind 0.0.0.0:8000`

## 📞 Support

For deployment issues, contact the development team.

**Current Database:** spacentraldata @ 82.25.109.137:3306
**Current Status:** ✅ Production Ready

