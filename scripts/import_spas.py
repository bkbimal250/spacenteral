"""
Script to import spas from CSV or JSON file

Usage:
    python manage.py shell < scripts/import_spas.py
    
Or run as a Django management command after creating one
"""

import os
import django
import json
import csv
from decimal import Decimal
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spa_central.settings')
django.setup()

from apps.spas.models import Spa
from apps.location.models import Area, City, State, Country
from apps.users.models import User
from django.utils.text import slugify


def import_spas_from_json(file_path):
    """Import spas from JSON file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    imported_count = 0
    errors = []
    
    for spa_data in data:
        try:
            # Get or create owner
            owner_email = spa_data.get('owner_email', 'admin@example.com')
            owner, _ = User.objects.get_or_create(
                email=owner_email,
                defaults={
                    'user_type': 'owner',
                    'first_name': 'Spa',
                    'last_name': 'Owner'
                }
            )
            
            # Get area
            area_name = spa_data.get('area')
            area = None
            if area_name:
                area = Area.objects.filter(name=area_name).first()
            
            # Create spa
            spa = Spa.objects.create(
                owner=owner,
                name=spa_data['name'],
                slug=slugify(spa_data['name']),
                description=spa_data.get('description', ''),
                area=area,
                address=spa_data.get('address', ''),
                latitude=spa_data.get('latitude'),
                longitude=spa_data.get('longitude'),
                phone=spa_data.get('phone', ''),
                email=spa_data.get('email', ''),
                website=spa_data.get('website'),
                status=spa_data.get('status', 'active'),
                rating=Decimal(spa_data.get('rating', '0.0')),
                amenities=spa_data.get('amenities', []),
                policies=spa_data.get('policies', {}),
            )
            
            imported_count += 1
            print(f"Imported: {spa.name}")
            
        except Exception as e:
            errors.append(f"Error importing {spa_data.get('name', 'Unknown')}: {str(e)}")
            print(f"Error: {str(e)}")
    
    print(f"\nImport Summary:")
    print(f"Successfully imported: {imported_count} spas")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nError Details:")
        for error in errors:
            print(f"  - {error}")


def import_spas_from_csv(file_path):
    """Import spas from CSV file"""
    
    imported_count = 0
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Get or create owner
                owner_email = row.get('owner_email', 'admin@example.com')
                owner, _ = User.objects.get_or_create(
                    email=owner_email,
                    defaults={
                        'user_type': 'owner',
                        'first_name': 'Spa',
                        'last_name': 'Owner'
                    }
                )
                
                # Get area
                area_name = row.get('area')
                area = None
                if area_name:
                    area = Area.objects.filter(name=area_name).first()
                
                # Create spa
                spa = Spa.objects.create(
                    owner=owner,
                    name=row['name'],
                    slug=slugify(row['name']),
                    description=row.get('description', ''),
                    area=area,
                    address=row.get('address', ''),
                    latitude=row.get('latitude') or None,
                    longitude=row.get('longitude') or None,
                    phone=row.get('phone', ''),
                    email=row.get('email', ''),
                    website=row.get('website') or None,
                    status=row.get('status', 'active'),
                    rating=Decimal(row.get('rating', '0.0')),
                )
                
                imported_count += 1
                print(f"Imported: {spa.name}")
                
            except Exception as e:
                errors.append(f"Error importing {row.get('name', 'Unknown')}: {str(e)}")
                print(f"Error: {str(e)}")
    
    print(f"\nImport Summary:")
    print(f"Successfully imported: {imported_count} spas")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nError Details:")
        for error in errors:
            print(f"  - {error}")


def create_sample_data():
    """Create sample spas for testing"""
    
    # Create a sample user (using email as primary identifier)
    owner, created = User.objects.get_or_create(
        email='owner@example.com',
        defaults={
            'user_type': 'owner',
            'first_name': 'Spa',
            'last_name': 'Owner'
        }
    )
    if created:
        owner.set_password('password123')
        owner.save()
    
    # Create sample spas
    sample_spas = [
        {
            'name': 'Luxury Wellness Spa',
            'description': 'Premium spa services with state-of-the-art facilities',
            'address': '123 Wellness Street',
            'phone': '+1234567890',
            'email': 'info@luxuryspa.com',
            'status': 'active',
            'rating': '4.5',
        },
        {
            'name': 'Serenity Day Spa',
            'description': 'Peaceful retreat for relaxation and rejuvenation',
            'address': '456 Serenity Lane',
            'phone': '+1234567891',
            'email': 'contact@serenityspa.com',
            'status': 'active',
            'rating': '4.8',
        },
        {
            'name': 'Urban Oasis Spa',
            'description': 'Modern spa in the heart of the city',
            'address': '789 Urban Plaza',
            'phone': '+1234567892',
            'email': 'hello@urbanoasis.com',
            'status': 'active',
            'rating': '4.3',
        },
    ]
    
    for spa_data in sample_spas:
        spa, created = Spa.objects.get_or_create(
            name=spa_data['name'],
            defaults={
                'owner': owner,
                'slug': slugify(spa_data['name']),
                'description': spa_data['description'],
                'address': spa_data['address'],
                'phone': spa_data['phone'],
                'email': spa_data['email'],
                'status': spa_data['status'],
                'rating': Decimal(spa_data['rating']),
            }
        )
        
        if created:
            print(f"Created sample spa: {spa.name}")
        else:
            print(f"Spa already exists: {spa.name}")


if __name__ == '__main__':
    print("Spa Import Script")
    print("=" * 50)
    
    # Example: Create sample data
    print("\nCreating sample data...")
    create_sample_data()
    
    # Example: Import from JSON file
    # import_spas_from_json('data/spas.json')
    
    # Example: Import from CSV file
    # import_spas_from_csv('data/spas.csv')

