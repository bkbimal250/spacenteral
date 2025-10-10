# SpaCentral Environment Variables Structure

## 📋 .env File Templates

### Development Environment (.env.development)

```env
# ===========================================
# SPACENTRAL DEVELOPMENT ENVIRONMENT
# ===========================================

# Django Settings
# ---------------
SECRET_KEY=django-insecure-qj1c-p**&$smg*@+0ie90$1lu&x#-k&#*m^5l*bx9eqctr4ha0
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*

# Database Configuration (MySQL)
# -------------------------------
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306

# CORS Configuration (Development - Allow All)
# --------------------------------------------
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000

# Security Settings (Development - Disabled)
# ------------------------------------------
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

# Email Configuration
# -------------------
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info.dishaonlinesoution@gmail.com
EMAIL_HOST_PASSWORD=ktrc uzzy upkr ftbv
DEFAULT_FROM_EMAIL=Disha Online Solution <info.dishaonlinesoution@gmail.com>

# Static & Media Files (Development)
# -----------------------------------
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media

# Application Settings
# --------------------
SITE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

# Logging
# -------
LOG_LEVEL=DEBUG
```

---

### Production Environment (.env.production)

```env
# ===========================================
# SPACENTRAL PRODUCTION ENVIRONMENT
# ===========================================

# Django Settings
# ---------------
SECRET_KEY=your-very-secure-random-secret-key-min-50-chars-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,82.25.109.137

# Database Configuration (MySQL Production)
# -----------------------------------------
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306

# CORS Configuration (Production - Restricted)
# --------------------------------------------
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com

# Security Settings (Production - Enabled)
# ----------------------------------------
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Email Configuration (Production)
# --------------------------------
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info.dishaonlinesoution@gmail.com
EMAIL_HOST_PASSWORD=ktrc uzzy upkr ftbv
DEFAULT_FROM_EMAIL=Disha Online Solution <info.dishaonlinesoution@gmail.com>
SERVER_EMAIL=info.dishaonlinesoution@gmail.com

# Static & Media Files (Production)
# ----------------------------------
STATIC_URL=/static/
STATIC_ROOT=/var/www/spacentral/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/spacentral/media

# Application Settings
# --------------------
SITE_URL=https://yourdomain.com
FRONTEND_URL=https://yourdomain.com
API_URL=https://yourdomain.com/api

# Logging
# -------
LOG_LEVEL=INFO
```

---

### Staging Environment (.env.staging)

```env
# ===========================================
# SPACENTRAL STAGING ENVIRONMENT
# ===========================================

# Django Settings
# ---------------
SECRET_KEY=your-staging-secret-key-different-from-production
DEBUG=False
ALLOWED_HOSTS=staging.yourdomain.com,82.25.109.137

# Database Configuration (MySQL Staging)
# --------------------------------------
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata_staging
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306

# CORS Configuration (Staging)
# ----------------------------
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://staging.yourdomain.com,http://localhost:5173

# Security Settings (Staging - Relaxed)
# -------------------------------------
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

# Email Configuration (Staging - Console)
# ---------------------------------------
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info.dishaonlinesoution@gmail.com
EMAIL_HOST_PASSWORD=ktrc uzzy upkr ftbv

# Static & Media Files (Staging)
# -------------------------------
STATIC_URL=/static/
STATIC_ROOT=/var/www/spacentral-staging/staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/spacentral-staging/media

# Application Settings
# --------------------
SITE_URL=https://staging.yourdomain.com
FRONTEND_URL=https://staging.yourdomain.com

# Logging
# -------
LOG_LEVEL=DEBUG
```

---

## 🔐 Environment Variable Descriptions

### Django Core Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Random 50+ character string |
| `DEBUG` | Debug mode toggle | `True` (dev), `False` (prod) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1,yourdomain.com` |

### Database Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `DB_ENGINE` | Database backend engine | `django.db.backends.mysql` |
| `DB_NAME` | Database name | `spacentraldata` |
| `DB_USER` | Database user | `dosadmin` |
| `DB_PASSWORD` | Database password | `DishaSolution@8989` |
| `DB_HOST` | Database host | `82.25.109.137` |
| `DB_PORT` | Database port | `3306` |

### CORS Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `CORS_ALLOW_ALL_ORIGINS` | Allow all origins | `True` (dev), `False` (prod) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed origins | `https://yourdomain.com` |

### Security Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS | `True` (prod), `False` (dev) |
| `SESSION_COOKIE_SECURE` | Use secure session cookies | `True` (prod), `False` (dev) |
| `CSRF_COOKIE_SECURE` | Use secure CSRF cookies | `True` (prod), `False` (dev) |
| `SECURE_HSTS_SECONDS` | HSTS max-age value | `31536000` (1 year) or `0` |

### Email Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `EMAIL_BACKEND` | Email backend to use | `smtp.EmailBackend` or `console.EmailBackend` |
| `EMAIL_HOST` | SMTP server host | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP server port | `587` (TLS) or `465` (SSL) |
| `EMAIL_USE_TLS` | Use TLS encryption | `True` |
| `EMAIL_HOST_USER` | SMTP username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | SMTP password/app password | Gmail app password |
| `DEFAULT_FROM_EMAIL` | Default from email | `YourApp <noreply@yourdomain.com>` |

### Static & Media Files

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `STATIC_URL` | URL prefix for static files | `/static/` |
| `STATIC_ROOT` | Absolute path to static files | `/var/www/spacentral/staticfiles` |
| `MEDIA_URL` | URL prefix for media files | `/media/` |
| `MEDIA_ROOT` | Absolute path to media files | `/var/www/spacentral/media` |

### Application Settings

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `SITE_URL` | Base URL of the site | `https://yourdomain.com` |
| `FRONTEND_URL` | Frontend application URL | `https://yourdomain.com` |
| `API_URL` | API base URL | `https://yourdomain.com/api` |

### Logging

| Variable | Description | Example Values |
|----------|-------------|----------------|
| `LOG_LEVEL` | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## 📝 How to Use

### 1. For Development (Local)

```bash
# Copy the development template
cp ENV_STRUCTURE.md .env

# Or create .env manually with development settings
nano .env

# Use DEBUG=True and CORS_ALLOW_ALL_ORIGINS=True
```

### 2. For Production (Server)

```bash
# On production server
nano /var/www/spacentral/.env

# Use production settings with:
# - DEBUG=False
# - Strong SECRET_KEY
# - Specific ALLOWED_HOSTS
# - SSL settings enabled
# - CORS restricted to your domain
```

### 3. For Staging

```bash
# Use staging template
# Separate database: spacentraldata_staging
# Relaxed security for testing
```

---

## 🔑 Generate Secure SECRET_KEY

```python
# Run in Django shell or Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use online generator:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## ⚠️ Security Best Practices

1. **Never commit .env files to Git**
   - Already in `.gitignore`
   - Use `.env.example` for templates only

2. **Use different SECRET_KEY for each environment**
   - Development: Can be simple
   - Production: Must be complex and secret

3. **Restrict CORS in production**
   - `CORS_ALLOW_ALL_ORIGINS=False`
   - Only list trusted domains

4. **Enable SSL in production**
   - `SECURE_SSL_REDIRECT=True`
   - Use HTTPS certificate

5. **Use strong database passwords**
   - Change default passwords
   - Use password manager

6. **Protect sensitive data**
   - Email passwords
   - API keys
   - Database credentials

---

## 🚀 Quick Setup Commands

### Development
```bash
# Create .env for development
cat > .env << 'EOF'
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
ALLOWED_HOSTS=localhost,127.0.0.1,*
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306
CORS_ALLOW_ALL_ORIGINS=True
EOF
```

### Production
```bash
# Create .env for production (replace values!)
cat > /var/www/spacentral/.env << 'EOF'
DEBUG=False
SECRET_KEY=REPLACE-WITH-SECURE-SECRET-KEY
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=spacentraldata
DB_USER=dosadmin
DB_PASSWORD=DishaSolution@8989
DB_HOST=82.25.109.137
DB_PORT=3306
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EOF
```

---

## 📂 File Locations

- **Development:** `./spa_central/.env`
- **Production:** `/var/www/spacentral/.env`
- **Staging:** `/var/www/spacentral-staging/.env`
- **Example:** `./.env.example` (safe to commit)

---

## ✅ Validation Checklist

Before deploying, verify:

- [ ] `.env` file exists in project root
- [ ] All required variables are set
- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS matches your domain
- [ ] Database credentials are correct
- [ ] CORS is properly restricted
- [ ] SSL settings enabled for HTTPS
- [ ] Email configuration tested
- [ ] File paths are absolute in production

---

## 🆘 Troubleshooting

### Environment variables not loading
```bash
# Check if python-decouple is installed
pip list | grep decouple

# Verify .env file exists
ls -la .env

# Check file permissions
chmod 600 .env
```

### Database connection errors
```bash
# Test MySQL connection
mysql -h 82.25.109.137 -u dosadmin -p spacentraldata

# Verify DB_* variables in .env
cat .env | grep DB_
```

### CORS errors in browser
```bash
# Check CORS settings
cat .env | grep CORS_

# Ensure frontend URL is in CORS_ALLOWED_ORIGINS
```

---

**Current Database:** spacentraldata @ 82.25.109.137:3306
**Status:** ✅ Production Ready

