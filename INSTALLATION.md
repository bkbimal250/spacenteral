# Installation Guide

This guide will help you set up the Spa Central project on your local machine or production server.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Setup](#docker-setup)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 12 or higher (optional, SQLite is used by default)
- Redis 6 or higher (for WebSocket and Celery)
- Docker and Docker Compose (for containerized setup)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd spa_central
```

### 2. Create Virtual Environment

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and update it with your settings:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For local development with SQLite (default)
# No need to configure database settings

# For PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=spa_central_db
DB_USER=spa_user
DB_PASSWORD=spa_password
DB_HOST=localhost
DB_PORT=5432

# Redis (required for WebSocket and Celery)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Database Setup

Run migrations to create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Create Sample Data (Optional)

```bash
python manage.py shell < scripts/import_spas.py
```

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

### 10. Run Redis (Required for WebSocket)

**On Linux/Mac:**
```bash
redis-server
```

**On Windows:**
Download and install Redis from [Redis for Windows](https://github.com/microsoftarchive/redis/releases)

### 11. Run Celery Worker (Optional)

In a separate terminal:

```bash
celery -A spa_central worker --loglevel=info
```

## Docker Setup

### 1. Prerequisites

- Docker
- Docker Compose

### 2. Build and Run

```bash
docker-compose up --build
```

This will start:
- Django application (port 8000)
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Celery worker

### 3. Run Migrations

```bash
docker-compose exec web python manage.py migrate
```

### 4. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Application

- Application: `http://localhost:8000/`
- Admin Panel: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`

### 6. Stop the Containers

```bash
docker-compose down
```

## Production Deployment

### 1. Environment Configuration

Update `.env` with production settings:

```env
SECRET_KEY=your-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=spa_central_prod
DB_USER=spa_user
DB_PASSWORD=secure_password
DB_HOST=db_host
DB_PORT=5432

# Redis
REDIS_HOST=redis_host
REDIS_PORT=6379

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install gunicorn
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start Application with Gunicorn

```bash
gunicorn spa_central.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 6. Start Daphne for WebSocket Support

```bash
daphne -b 0.0.0.0 -p 8001 spa_central.asgi:application
```

### 7. Configure Nginx (Recommended)

Create a Nginx configuration file:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static/ {
        alias /path/to/spa_central/staticfiles/;
    }

    location /media/ {
        alias /path/to/spa_central/media/;
    }
}
```

### 8. Setup Systemd Service (Linux)

Create `/etc/systemd/system/spa_central.service`:

```ini
[Unit]
Description=Spa Central Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/spa_central
ExecStart=/path/to/venv/bin/gunicorn spa_central.wsgi:application --bind 0.0.0.0:8000 --workers 4

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable spa_central
sudo systemctl start spa_central
```

## Troubleshooting

### Database Connection Error

**Issue:** Cannot connect to PostgreSQL database

**Solution:**
1. Ensure PostgreSQL is running
2. Check database credentials in `.env`
3. Verify database exists: `createdb spa_central_db`

### Redis Connection Error

**Issue:** Cannot connect to Redis

**Solution:**
1. Ensure Redis is running: `redis-cli ping`
2. Check Redis host and port in `.env`

### Static Files Not Loading

**Issue:** Static files return 404

**Solution:**
1. Run `python manage.py collectstatic`
2. Check `STATIC_ROOT` and `STATIC_URL` in settings
3. Configure web server to serve static files

### Migration Errors

**Issue:** Migration conflicts

**Solution:**
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Permission Errors

**Issue:** Permission denied on media/static directories

**Solution:**
```bash
sudo chown -R www-data:www-data /path/to/spa_central/media
sudo chown -R www-data:www-data /path/to/spa_central/staticfiles
```

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/)
- [Celery Documentation](https://docs.celeryproject.org/)

## Support

For issues and questions, please open an issue on GitHub or contact the development team.

