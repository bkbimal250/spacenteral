# Location API Guide

This guide explains the Location Management API for States, Cities, and Areas.

## 📍 Overview

The location system follows a hierarchical structure:
```
State → City → Area
```

Each level is connected:
- **States** are top-level (e.g., "California", "New York")
- **Cities** belong to States (e.g., "Los Angeles" in "California")
- **Areas** belong to Cities (e.g., "Downtown" in "Los Angeles")

## 🔌 API Endpoints

### States

**List all states:**
```http
GET /api/states/
```

**Create a state:**
```http
POST /api/states/
Content-Type: application/json

{
    "name": "California"
}
```

**Get state details:**
```http
GET /api/states/{id}/
```

**Update a state:**
```http
PATCH /api/states/{id}/
Content-Type: application/json

{
    "name": "California Updated"
}
```

**Delete a state:**
```http
DELETE /api/states/{id}/
```

**Search states:**
```http
GET /api/states/?search=Cali
```

---

### Cities

**List all cities:**
```http
GET /api/cities/
```

**Filter cities by state:**
```http
GET /api/cities/?state=1
```

**Create a city:**
```http
POST /api/cities/
Content-Type: application/json

{
    "name": "Los Angeles",
    "state": 1
}
```

**Get city details:**
```http
GET /api/cities/{id}/
```

**Response includes state name:**
```json
{
    "id": 1,
    "name": "Los Angeles",
    "state": 1,
    "state_name": "California",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
}
```

**Update a city:**
```http
PATCH /api/cities/{id}/
Content-Type: application/json

{
    "name": "Los Angeles Updated",
    "state": 1
}
```

**Delete a city:**
```http
DELETE /api/cities/{id}/
```

**Search cities:**
```http
GET /api/cities/?search=Los
```

---

### Areas

**List all areas:**
```http
GET /api/areas/
```

**Filter areas by city:**
```http
GET /api/areas/?city=1
```

**Filter areas by state:**
```http
GET /api/areas/?city__state=1
```

**Create an area:**
```http
POST /api/areas/
Content-Type: application/json

{
    "name": "Downtown",
    "city": 1
}
```

**Get area details:**
```http
GET /api/areas/{id}/
```

**Response includes city and state names:**
```json
{
    "id": 1,
    "name": "Downtown",
    "city": 1,
    "city_name": "Los Angeles",
    "state_name": "California",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
}
```

**Update an area:**
```http
PATCH /api/areas/{id}/
Content-Type: application/json

{
    "name": "Downtown Updated",
    "city": 1
}
```

**Delete an area:**
```http
DELETE /api/areas/{id}/
```

**Search areas:**
```http
GET /api/areas/?search=Down
```

---

## 🔍 Search & Filter Features

### Search
All endpoints support the `search` parameter:
- **States**: Searches by name
- **Cities**: Searches by name and state name
- **Areas**: Searches by name, city name, and state name

Examples:
```http
GET /api/states/?search=Cali
GET /api/cities/?search=Angeles
GET /api/areas/?search=Downtown
```

### Filtering
- **Cities** can be filtered by `state` ID
- **Areas** can be filtered by `city` ID or `city__state` ID

Examples:
```http
GET /api/cities/?state=1
GET /api/areas/?city=1
GET /api/areas/?city__state=1
```

### Ordering
All endpoints support ordering:
```http
GET /api/states/?ordering=name
GET /api/states/?ordering=-created_at
GET /api/cities/?ordering=state,name
```

---

## 📊 Model Structure

### State Model
```python
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### City Model
```python
class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='cities', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'state')
```

### Area Model
```python
class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='areas', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'city')
```

---

## 🔐 Validation Rules

### State
- **Name**: Required, unique, max 100 characters

### City
- **Name**: Required, max 100 characters
- **State**: Required (foreign key)
- **Unique constraint**: City name must be unique within a state

### Area
- **Name**: Required, max 100 characters
- **City**: Required (foreign key)
- **Unique constraint**: Area name must be unique within a city

---

## 🚨 Error Responses

### Duplicate Name
```json
{
    "name": ["state with this name already exists."]
}
```

### Missing Required Field
```json
{
    "state": ["This field is required."]
}
```

### Invalid Foreign Key
```json
{
    "state": ["Invalid pk \"999\" - object does not exist."]
}
```

### Protected Deletion
When trying to delete a state/city that has related cities/areas:
```json
{
    "detail": "Cannot delete because it has related records."
}
```

---

## 💡 Usage Examples

### Create Complete Hierarchy

**Step 1: Create a State**
```http
POST /api/states/
{"name": "California"}
```
Response: `{"id": 1, "name": "California", ...}`

**Step 2: Create a City**
```http
POST /api/cities/
{"name": "Los Angeles", "state": 1}
```
Response: `{"id": 1, "name": "Los Angeles", "state": 1, "state_name": "California", ...}`

**Step 3: Create an Area**
```http
POST /api/areas/
{"name": "Downtown", "city": 1}
```
Response: `{"id": 1, "name": "Downtown", "city": 1, "city_name": "Los Angeles", "state_name": "California", ...}`

---

## 🎯 Frontend Integration

The admin dashboard provides full CRUD interface:

1. **Navigate to Locations** (`/locations`)
2. **Switch between tabs**: States, Cities, Areas
3. **Add new**: Click "+ Add State/City/Area"
4. **Edit**: Click "Edit" button
5. **Delete**: Click "Delete" button (with confirmation)
6. **Search**: Use search box to filter

---

## 📝 Notes

- States can only be deleted if they have no cities
- Cities can only be deleted if they have no areas
- Deletion uses `PROTECT` to prevent accidental data loss
- All timestamps are automatically managed
- Names are case-sensitive

---

## 🔗 Related

- Spas use Areas for location
- Machines are installed in Areas
- All location data accessible via Django Admin

