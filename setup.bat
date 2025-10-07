@echo off

REM Spa Central Setup Script for Windows

echo =========================================
echo Spa Central - Setup Script (Windows)
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please update .env file with your configurations
)

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
set /p create_superuser=Would you like to create a superuser? (y/n): 
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo =========================================
echo Setup completed successfully!
echo =========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo To access the admin panel:
echo   http://localhost:8000/admin/
echo.
echo To access the API:
echo   http://localhost:8000/api/
echo.

pause

