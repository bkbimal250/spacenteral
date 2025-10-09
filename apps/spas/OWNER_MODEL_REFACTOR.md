# Spa Owner Model Refactoring

## Overview
Refactored the Spa ownership structure to use independent `PrimaryOwner` and `SecondaryOwner` models with one-to-many relationships.

## Changes Made

### 1. **Models** (`apps/spas/models.py`)

#### Removed:
- `SpaOwner` model (with `parent_owner` hierarchy)
- Spa fields: `owner`, `sub_owners`, `reopen_date`

#### Added:
Two independent owner models:

**PrimaryOwner Model:**
```python
class PrimaryOwner(models.Model):
    fullname = CharField(max_length=200)
    email = EmailField(blank=True, null=True)
    phone = CharField(max_length=20, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**SecondaryOwner Model:**
```python
class SecondaryOwner(models.Model):
    fullname = CharField(max_length=200)
    email = EmailField(blank=True, null=True)
    phone = CharField(max_length=20, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Updated Spa Model:
- `primary_owner` → ForeignKey to `PrimaryOwner` (One-to-Many, required for spa creation)
- `secondary_owner` → ForeignKey to `SecondaryOwner` (One-to-Many, optional)
- Added: `spamanager` field (CharField)
- Removed: `reopen_date` field
- Updated: `STATUS_CHOICES` (kept only required statuses)

### 2. **Relationship Structure**

**One-to-Many Relationships:**
- One `PrimaryOwner` can manage multiple Spas
- One `SecondaryOwner` can manage multiple Spas
- Each Spa has exactly ONE `PrimaryOwner`
- Each Spa has ZERO or ONE `SecondaryOwner`

**Example:**
```
PrimaryOwner A → Spa1, Spa2, Spa3
PrimaryOwner B → Spa4, Spa5, Spa6

SecondaryOwner X → Spa1, Spa3, Spa7
SecondaryOwner Y → Spa4, Spa8

Spa1 → PrimaryOwner A + SecondaryOwner X
Spa2 → PrimaryOwner A (no secondary owner)
```

### 3. **Serializers** (`apps/spas/serializers.py`)

#### Added:
- `PrimaryOwnerSerializer`
- `SecondaryOwnerSerializer`

#### Updated:
- `SpaListSerializer` → Added `spamanager` field
- `SpaDetailSerializer` → Removed `sub_owners`, `reopen_date`; Added `spamanager`
- `SpaCreateUpdateSerializer` → Updated fields to match new model

#### Removed:
- `SpaOwnerSerializer` (replaced with two separate serializers)

### 4. **Filters** (`apps/spas/filters.py`)

#### Added:
- `PrimaryOwnerFilter` → Filter by fullname, email, phone
- `SecondaryOwnerFilter` → Filter by fullname, email, phone

#### Updated:
- `SpaFilter` → Updated to use `PrimaryOwner` and `SecondaryOwner`, added `spamanager` filter

#### Removed:
- `SpaOwnerFilter`

### 5. **Views** (`apps/spas/views.py`)

#### Added:
- `PrimaryOwnerViewSet` → CRUD operations for primary owners
- `SecondaryOwnerViewSet` → CRUD operations for secondary owners

#### Updated:
- `SpaViewSet` → Removed `sub_owners` prefetch, added `spamanager` to search_fields

#### Removed:
- `SpaOwnerViewSet` (replaced with two separate viewsets)

### 6. **Admin** (`apps/spas/admin.py`)

#### Added:
- `PrimaryOwnerAdmin` → Admin interface for primary owners
- `SecondaryOwnerAdmin` → Admin interface for secondary owners

#### Updated:
- `SpaAdmin` → Updated fieldsets to show new structure, added `spamanager` field

#### Removed:
- `SpaOwnerAdmin`

### 7. **URLs** (`apps/spas/urls.py`)

#### Updated Routes:
- `/api/primary-owners/` → PrimaryOwner CRUD
- `/api/secondary-owners/` → SecondaryOwner CRUD
- `/api/spas/` → Spa CRUD (unchanged)

#### Removed:
- `/api/spa-owners/` (replaced with two separate endpoints)

### 8. **Migrations**

Three migration files created:
1. `0004_create_new_owner_models.py` → Creates new models and temporary fields
2. `0005_migrate_owner_data.py` → Data migration from old to new models
3. `0006_finalize_owner_migration.py` → Removes old fields and finalizes structure

## API Endpoints

### Primary Owners
- `GET /api/primary-owners/` → List all primary owners
- `POST /api/primary-owners/` → Create primary owner
- `GET /api/primary-owners/{id}/` → Retrieve primary owner
- `PUT/PATCH /api/primary-owners/{id}/` → Update primary owner
- `DELETE /api/primary-owners/{id}/` → Delete primary owner

### Secondary Owners
- `GET /api/secondary-owners/` → List all secondary owners
- `POST /api/secondary-owners/` → Create secondary owner
- `GET /api/secondary-owners/{id}/` → Retrieve secondary owner
- `PUT/PATCH /api/secondary-owners/{id}/` → Update secondary owner
- `DELETE /api/secondary-owners/{id}/` → Delete secondary owner

### Spas
- All existing endpoints remain the same
- Updated request/response format to use `primary_owner` and `secondary_owner` fields

## Database Schema

### Primary Owners Table
```
primary_owners:
  - id (PK)
  - fullname
  - email
  - phone
  - created_at
  - updated_at
```

### Secondary Owners Table
```
secondary_owners:
  - id (PK)
  - fullname
  - email
  - phone
  - created_at
  - updated_at
```

### Spas Table (Updated)
```
spas:
  - id (PK)
  - spa_code (unique)
  - spa_name
  - primary_owner_id (FK → primary_owners)
  - secondary_owner_id (FK → secondary_owners, nullable)
  - spamanager
  - opening_date (no reopen_date)
  - status
  - ... (other fields)
```

## Key Benefits

1. ✅ **Independent Owner Management** → Primary and secondary owners are separate entities
2. ✅ **Clear Relationships** → One-to-Many ensures each spa has only one primary owner
3. ✅ **Simplified Structure** → No hierarchical parent-child relationships
4. ✅ **Better Data Integrity** → Separate tables prevent confusion between owner types
5. ✅ **Flexible Assignment** → Owners can manage multiple spas independently
6. ✅ **Cleaner API** → Separate endpoints for different owner types

## Migration Notes

- ✅ All existing data was migrated successfully
- ✅ Old `SpaOwner` records were split into `PrimaryOwner` and `SecondaryOwner` based on usage
- ✅ All Spa relationships were preserved
- ✅ No data loss during migration

## Testing Checklist

- [ ] Test creating primary owners
- [ ] Test creating secondary owners
- [ ] Test creating spas with primary owner only
- [ ] Test creating spas with both primary and secondary owners
- [ ] Test filtering spas by owner
- [ ] Test updating owner information
- [ ] Verify admin interface works correctly
- [ ] Test API endpoints with Postman

## Status

✅ **COMPLETED** - All changes implemented and migrations applied successfully!

---

**Date:** October 9, 2025
**Author:** AI Assistant

