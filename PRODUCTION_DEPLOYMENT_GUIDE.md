# Production Deployment Guide

## 🚀 Complete Production Deployment Checklist

**Last Updated:** October 15, 2025  
**Status:** ✅ READY FOR PRODUCTION

---

## 📊 **YOUR PRODUCTION SETUP**

### **Domains:**
- **Admin Dashboard:** `https://infodocs.dishaonlinesolution.in`
- **Manager Dashboard:** `https://machspa.dishaonlinesolution.in`
- **Backend API:** Your backend server (configure below)

### **Configured In settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://infodocs.dishaonlinesolution.in",
    "https://machspa.dishaonlinesolution.in",
]

CSRF_TRUSTED_ORIGINS = [
    "https://infodocs.dishaonlinesolution.in",
    "https://machspa.dishaonlinesolution.in",
]

ALLOWED_HOSTS = [
    'infodocs.dishaonlinesolution.in',
    'machspa.dishaonlinesolution.in',
]
```

---

## 🔧 **STEP-BY-STEP DEPLOYMENT**

### **STEP 1: Prepare Environment File**

Create `.env` in project root:

```env
# ============================================================================
# PRODUCTION CONFIGURATION
# ============================================================================

DEBUG=False
SECRET_KEY=GENERATE_NEW_SECRET_KEY_HERE

# Allowed Hosts
ALLOWED_HOSTS=infodocs.dishaonlinesolution.in,machspa.dishaonlinesolution.in,your-backend-domain.com

# Database
DB_ENGINE=django.db.backends.mysql
DB_NAME=spa_central_production
DB_USER=spa_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=3306

# Email (Gmail)
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Redis (for WebSocket)
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

#### **Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### **STEP 2: Install System Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install MySQL
sudo apt install mysql-server -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y

# Install Node.js (for frontend builds)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

---

### **STEP 3: Setup Database**

```bash
# Login to MySQL
sudo mysql -u root -p

# Create database and user
CREATE DATABASE spa_central_production CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'spa_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON spa_central_production.* TO 'spa_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### **STEP 4: Deploy Backend**

```bash
# Clone repository
cd /var/www/
git clone your-repository-url spa_central
cd spa_central

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file (use template above)
nano .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Set user_type = 'admin'

# Collect static files
python manage.py collectstatic --noinput

# Create logs directory
mkdir -p logs
chmod 755 logs

# Test deployment check
python manage.py check --deploy
```

---

### **STEP 5: Build Frontend Dashboards**

#### **Admin Dashboard:**
```bash
cd frontend/Dashboard/admindashbboard

# Create .env.production
echo "VITE_API_BASE_URL=https://your-backend-api.com/api" > .env.production

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in dist/ folder
# Deploy dist/ to: https://infodocs.dishaonlinesolution.in
```

#### **Manager Dashboard:**
```bash
cd frontend/Dashboard/managerdashboard

# Create .env.production
echo "VITE_API_BASE_URL=https://your-backend-api.com/api" > .env.production

# Install dependencies
npm install

# Build for production
npm run build

# Output will be in dist/ folder
# Deploy dist/ to: https://machspa.dishaonlinesolution.in
```

---

### **STEP 6: Configure Gunicorn**

Create `/etc/systemd/system/spacentral.service`:

```ini
[Unit]
Description=Spa Central Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/spa_central
Environment="PATH=/var/www/spa_central/venv/bin"
ExecStart=/var/www/spa_central/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          --timeout 120 \
          --access-logfile /var/www/spa_central/logs/gunicorn_access.log \
          --error-logfile /var/www/spa_central/logs/gunicorn_error.log \
          spa_central.wsgi:application

[Install]
WantedBy=multi-user.target
```

---

### **STEP 7: Configure Daphne (WebSocket)**

Create `/etc/systemd/system/daphne.service`:

```ini
[Unit]
Description=Spa Central Daphne (WebSocket) Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/spa_central
Environment="PATH=/var/www/spa_central/venv/bin"
ExecStart=/var/www/spa_central/venv/bin/daphne \
          -b 127.0.0.1 \
          -p 8001 \
          spa_central.asgi:application

[Install]
WantedBy=multi-user.target
```

---

### **STEP 8: Start Services**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start Gunicorn
sudo systemctl start spacentral
sudo systemctl enable spacentral

# Start Daphne
sudo systemctl start daphne
sudo systemctl enable daphne

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Check status
sudo systemctl status spacentral
sudo systemctl status daphne
sudo systemctl status redis
```

---

### **STEP 9: Configure Nginx**

Create `/etc/nginx/sites-available/spacentral`:

```nginx
# Admin Dashboard - infodocs.dishaonlinesolution.in
server {
    listen 80;
    server_name infodocs.dishaonlinesolution.in;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name infodocs.dishaonlinesolution.in;
    
    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/infodocs.dishaonlinesolution.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/infodocs.dishaonlinesolution.in/privkey.pem;
    
    # Serve React build
    root /var/www/spa_central/frontend/Dashboard/admindashbboard/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# Manager Dashboard - machspa.dishaonlinesolution.in
server {
    listen 80;
    server_name machspa.dishaonlinesolution.in;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name machspa.dishaonlinesolution.in;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/machspa.dishaonlinesolution.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/machspa.dishaonlinesolution.in/privkey.pem;
    
    # Serve React build
    root /var/www/spa_central/frontend/Dashboard/managerdashboard/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}

# Backend API Server
server {
    listen 80;
    server_name your-backend-api.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-backend-api.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-backend-api.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-backend-api.com/privkey.pem;
    
    client_max_body_size 30M;
    
    # Static files
    location /static/ {
        alias /var/www/spa_central/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/spa_central/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # WebSocket (Daphne)
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API and Admin (Gunicorn)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### **Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/spacentral /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### **STEP 10: SSL Certificates**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificates
sudo certbot --nginx -d infodocs.dishaonlinesolution.in
sudo certbot --nginx -d machspa.dishaonlinesolution.in
sudo certbot --nginx -d your-backend-api.com

# Test auto-renewal
sudo certbot renew --dry-run
```

---

### **STEP 11: Setup Cron Jobs**

```bash
# Edit crontab
crontab -e

# Add these lines:
# Delete expired tokens daily at 2 AM
0 2 * * * cd /var/www/spa_central && /var/www/spa_central/venv/bin/python manage.py delete_expired_tokens --days 7

# Renew SSL certificates (runs twice daily)
0 0,12 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
```

---

## ✅ **POST-DEPLOYMENT VERIFICATION**

### 1. **Test Backend API:**
```bash
# Health check
curl https://your-backend-api.com/api/

# Test authentication
curl -X POST https://your-backend-api.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
```

### 2. **Test Frontend Dashboards:**
```bash
# Admin Dashboard
curl -I https://infodocs.dishaonlinesolution.in

# Manager Dashboard
curl -I https://machspa.dishaonlinesolution.in
```

### 3. **Test Security Headers:**
```bash
curl -I https://your-backend-api.com | grep -i "strict-transport\|x-frame\|x-content"
```

Should show:
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-Content-Type-Options`

### 4. **Test WebSocket:**
```bash
# Check Daphne is running
sudo systemctl status daphne

# Test WebSocket connection (from browser console)
const ws = new WebSocket('wss://your-backend-api.com/ws/chat/1/?token=YOUR_TOKEN');
ws.onopen = () => console.log('Connected!');
```

### 5. **Test CORS:**
```bash
curl -H "Origin: https://infodocs.dishaonlinesolution.in" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: authorization,content-type" \
     -X OPTIONS \
     https://your-backend-api.com/api/users/
```

Should return: `Access-Control-Allow-Origin: https://infodocs.dishaonlinesolution.in`

---

## 🔒 **SECURITY VERIFICATION**

### Run Django Security Check:
```bash
cd /var/www/spa_central
source venv/bin/activate
python manage.py check --deploy
```

**All checks should PASS when DEBUG=False!**

### Verify Settings:
```bash
# Check DEBUG is False
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
False  # Should be False!
>>> settings.ALLOWED_HOSTS
['infodocs.dishaonlinesolution.in', 'machspa.dishaonlinesolution.in', ...]
>>> settings.CORS_ALLOWED_ORIGINS
['https://infodocs.dishaonlinesolution.in', 'https://machspa.dishaonlinesolution.in']
>>> exit()
```

---

## 📝 **ENVIRONMENT VARIABLES CHECKLIST**

Required in `.env`:

- [x] DEBUG=False
- [x] SECRET_KEY (new, strong key)
- [x] ALLOWED_HOSTS (your domains)
- [x] DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- [x] EMAIL_HOST_PASSWORD
- [x] REDIS_HOST, REDIS_PORT (optional, defaults to localhost)
- [x] SECURE_SSL_REDIRECT=True
- [x] SESSION_COOKIE_SECURE=True
- [x] CSRF_COOKIE_SECURE=True

---

## 🌐 **FRONTEND DEPLOYMENT**

### **Admin Dashboard** (infodocs.dishaonlinesolution.in):

1. **Build:**
```bash
cd frontend/Dashboard/admindashbboard
echo "VITE_API_BASE_URL=https://your-backend-api.com/api" > .env.production
npm install
npm run build
```

2. **Deploy:**
```bash
# Copy dist/ contents to server
scp -r dist/* user@server:/var/www/spa_central/frontend/Dashboard/admindashbboard/dist/

# Or via Hostinger file manager:
# Upload dist/ contents to public_html for infodocs.dishaonlinesolution.in
```

### **Manager Dashboard** (machspa.dishaonlinesolution.in):

1. **Build:**
```bash
cd frontend/Dashboard/managerdashboard
echo "VITE_API_BASE_URL=https://your-backend-api.com/api" > .env.production
npm install
npm run build
```

2. **Deploy:**
```bash
# Copy dist/ contents to server
scp -r dist/* user@server:/var/www/spa_central/frontend/Dashboard/managerdashboard/dist/

# Or via Hostinger:
# Upload dist/ contents to public_html for machspa.dishaonlinesolution.in
```

---

## 📊 **SERVICE STATUS MONITORING**

### Check All Services:
```bash
# Gunicorn (Django HTTP)
sudo systemctl status spacentral

# Daphne (WebSocket)
sudo systemctl status daphne

# Nginx (Web Server)
sudo systemctl status nginx

# Redis (Channel Layer)
sudo systemctl status redis

# MySQL (Database)
sudo systemctl status mysql
```

### View Logs:
```bash
# Django logs
tail -f /var/www/spa_central/logs/django.log

# Gunicorn logs
tail -f /var/www/spa_central/logs/gunicorn_error.log

# Nginx logs
tail -f /var/log/nginx/error.log

# Daphne logs
journalctl -u daphne -f
```

---

## 🔄 **UPDATE/MAINTENANCE**

### Deploy Code Updates:
```bash
cd /var/www/spa_central
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart spacentral
sudo systemctl restart daphne
```

### Deploy Frontend Updates:
```bash
# Build new version
cd frontend/Dashboard/admindashbboard
npm run build

# Upload to server or Hostinger
# Replace old dist/ with new one
```

---

## 🧪 **TESTING IN PRODUCTION**

### 1. **Test Admin Login:**
- Go to: `https://infodocs.dishaonlinesolution.in`
- Login with admin credentials
- Verify dashboard loads
- Test CRUD operations
- Test file uploads

### 2. **Test Manager Login:**
- Go to: `https://machspa.dishaonlinesolution.in`
- Login with manager credentials
- Verify dashboard loads
- Test features

### 3. **Test WebSocket Chat:**
- Open FloatingChat
- Send message
- Verify real-time delivery

### 4. **Test Rate Limiting:**
- Try logging in 6 times quickly
- 6th attempt should fail with "429 Too Many Requests"

### 5. **Test File Upload:**
- Upload PDF (should work)
- Try uploading .exe (should fail)
- Upload 35MB file (should fail - max 30MB)

---

## 🚨 **TROUBLESHOOTING**

### Issue: 502 Bad Gateway
**Solution:**
```bash
sudo systemctl restart spacentral
sudo systemctl restart daphne
sudo systemctl restart nginx
```

### Issue: CORS errors
**Solution:**
- Verify domains in `CORS_ALLOWED_ORIGINS`
- Check frontend `.env.production` has correct API URL
- Restart services

### Issue: WebSocket not connecting
**Solution:**
```bash
# Check Daphne is running
sudo systemctl status daphne

# Check Redis is running
redis-cli ping

# Check firewall allows WebSocket
```

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart spacentral
```

### Issue: Database connection error
**Solution:**
- Verify database credentials in .env
- Check database is running: `sudo systemctl status mysql`
- Test connection: `python manage.py dbshell`

---

## 📈 **PERFORMANCE OPTIMIZATION**

### 1. **Database:**
```sql
-- Add indexes for better performance
-- Already done in models.py
```

### 2. **Redis Configuration:**
```bash
# Edit redis.conf for production
sudo nano /etc/redis/redis.conf

# Set:
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### 3. **Gunicorn Workers:**
```bash
# Formula: (2 × CPU cores) + 1
# For 2 CPU cores: 5 workers
--workers 5
```

---

## 🎯 **FINAL CHECKLIST**

Before going live:

- [ ] DEBUG=False in .env
- [ ] Strong SECRET_KEY generated
- [ ] Database configured and migrated
- [ ] Redis installed and running
- [ ] Static files collected
- [ ] Media directory writable
- [ ] SSL certificates installed
- [ ] Nginx configured and running
- [ ] Gunicorn service running
- [ ] Daphne service running
- [ ] Frontend builds deployed
- [ ] Admin user created
- [ ] Test users created (manager, spa_manager)
- [ ] All tests passing
- [ ] `python manage.py check --deploy` passes
- [ ] Backup system configured
- [ ] Monitoring set up
- [ ] Error tracking configured (Sentry)

---

## 🆘 **SUPPORT & MONITORING**

### Set Up Monitoring:
```bash
# Install monitoring tools
pip install sentry-sdk

# Add to settings.py:
if not DEBUG:
    import sentry_sdk
    sentry_sdk.init(dsn='your-sentry-dsn')
```

### Database Backups:
```bash
# Add to crontab
0 3 * * * mysqldump -u spa_user -p'password' spa_central_production > /backups/db_$(date +\%Y\%m\%d).sql
```

---

## 🎉 **PRODUCTION READY!**

Your settings.py is now:
- ✅ Security hardened
- ✅ Production optimized
- ✅ CORS configured for your domains
- ✅ CSRF protection enabled
- ✅ All duplicates removed
- ✅ Well organized
- ✅ Properly documented

**Status: READY TO DEPLOY! 🚀**

---

**Deployment Date:** _____________  
**Deployed By:** _____________  
**Version:** 1.0.0 Production

