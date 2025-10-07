#!/bin/bash

# Spa Central Setup Script

echo "========================================="
echo "Spa Central - Setup Script"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env file with your configurations"
fi

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Would you like to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "To access the admin panel:"
echo "  http://localhost:8000/admin/"
echo ""
echo "To access the API:"
echo "  http://localhost:8000/api/"
echo ""

