# Spa Manager API Testing Guide

## Quick Test Commands

### Prerequisites
Make sure your Django server is running:
```bash
python manage.py runserver
```

---

## Testing Spa Manager API

### 1. Create a Spa Manager
```bash
# Using axios (as per user preference)
POST http://localhost:8000/api/spa-managers/

Body (JSON):
{
  "fullname": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main Street",
  "spa": 1
}
```

**Expected Response (201 Created):**
```json
{
  "fullname": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main Street",
  "spa": 1
}
```

---

### 2. List All Spa Managers
```bash
GET http://localhost:8000/api/spa-managers/
```

**Expected Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "fullname": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "spa": 1,
      "spa_name": "Luxury Spa",
      "spa_code": "SPA001",
      "created_at": "2025-10-15T10:30:00Z"
    }
  ]
}
```

---

### 3. Get Spa Manager Details
```bash
GET http://localhost:8000/api/spa-managers/1/
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "fullname": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main Street",
  "spa": 1,
  "spa_name": "Luxury Spa",
  "spa_code": "SPA001",
  "document_count": 5,
  "created_at": "2025-10-15T10:30:00Z",
  "updated_at": "2025-10-15T10:30:00Z"
}
```

---

### 4. Update Spa Manager
```bash
PATCH http://localhost:8000/api/spa-managers/1/

Body (JSON):
{
  "phone": "+9876543210"
}
```

---

### 5. Get Managers by Spa
```bash
GET http://localhost:8000/api/spa-managers/by_spa/?spa_id=1
```

---

### 6. Search Spa Managers
```bash
GET http://localhost:8000/api/spa-managers/?search=John
```

---

### 7. Filter Spa Managers
```bash
# By email
GET http://localhost:8000/api/spa-managers/?email=john

# By spa
GET http://localhost:8000/api/spa-managers/?spa=1
```

---

### 8. Get Spa Manager Statistics
```bash
GET http://localhost:8000/api/spa-managers/statistics/
```

**Expected Response:**
```json
{
  "total_managers": 10,
  "managers_with_spa": 8,
  "managers_without_spa": 2,
  "top_spas_by_manager_count": [
    {
      "spa__spa_name": "Luxury Spa",
      "spa__spa_code": "SPA001",
      "manager_count": 3
    }
  ]
}
```

---

### 9. Delete Spa Manager
```bash
DELETE http://localhost:8000/api/spa-managers/1/
```

**Expected Response (204 No Content)**

---

## Testing Spa Manager Document API

### 1. Upload Document for Spa Manager
```bash
POST http://localhost:8000/api/spa-manager-documents/

Body (multipart/form-data):
{
  "title": "Manager Contract",
  "spa_manager": 1,
  "file": <file upload>,
  "notes": "Employment contract for John Doe"
}
```

**Expected Response (201 Created):**
```json
{
  "title": "Manager Contract",
  "spa_manager": 1,
  "file": "/media/documents/spa_manager_1/contract.pdf",
  "notes": "Employment contract for John Doe"
}
```

---

### 2. List All Documents
```bash
GET http://localhost:8000/api/spa-manager-documents/
```

**Expected Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Manager Contract",
      "file": "/media/documents/spa_manager_1/contract.pdf",
      "notes": "Employment contract for John Doe",
      "spa_manager": 1,
      "manager_name": "John Doe",
      "spa_name": "Luxury Spa",
      "spa_code": "SPA001",
      "uploaded_by": 1,
      "uploaded_by_name": "Admin User",
      "file_size": "245.3 KB",
      "file_extension": "PDF",
      "created_at": "2025-10-15T10:35:00Z",
      "updated_at": "2025-10-15T10:35:00Z"
    }
  ]
}
```

---

### 3. Get Document Details
```bash
GET http://localhost:8000/api/spa-manager-documents/1/
```

---

### 4. Download Document
```bash
GET http://localhost:8000/api/spa-manager-documents/1/download/
```

**Response:** File download

---

### 5. Get Documents by Manager
```bash
GET http://localhost:8000/api/spa-manager-documents/by_manager/?manager_id=1
```

---

### 6. Filter Documents
```bash
# By manager
GET http://localhost:8000/api/spa-manager-documents/?spa_manager=1

# By file extension
GET http://localhost:8000/api/spa-manager-documents/?file_ext=pdf

# By title
GET http://localhost:8000/api/spa-manager-documents/?title=contract

# By date range
GET http://localhost:8000/api/spa-manager-documents/?created_from=2025-01-01&created_to=2025-12-31
```

---

### 7. Search Documents
```bash
GET http://localhost:8000/api/spa-manager-documents/?search=contract
```

---

### 8. Get Document Statistics
```bash
GET http://localhost:8000/api/spa-manager-documents/statistics/
```

**Expected Response:**
```json
{
  "total_documents": 50,
  "top_managers_by_document_count": [
    {
      "spa_manager__fullname": "John Doe",
      "count": 15
    }
  ],
  "top_uploaders": [
    {
      "uploaded_by__email": "admin@example.com",
      "count": 30
    }
  ]
}
```

---

### 9. Update Document
```bash
PATCH http://localhost:8000/api/spa-manager-documents/1/

Body (JSON):
{
  "notes": "Updated notes"
}
```

---

### 10. Delete Document
```bash
DELETE http://localhost:8000/api/spa-manager-documents/1/
```

**Expected Response (204 No Content)**

---

## Using Axios (User Preference)

### Example: Create Spa Manager
```javascript
import axios from 'axios';

const createSpaManager = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/spa-managers/', {
      fullname: 'John Doe',
      email: 'john.doe@example.com',
      phone: '+1234567890',
      address: '123 Main Street',
      spa: 1
    });
    console.log('Manager created:', response.data);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

---

### Example: Upload Document
```javascript
import axios from 'axios';

const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('title', 'Manager Contract');
    formData.append('spa_manager', 1);
    formData.append('file', file);
    formData.append('notes', 'Employment contract');

    const response = await axios.post(
      'http://localhost:8000/api/spa-manager-documents/', 
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    console.log('Document uploaded:', response.data);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

---

### Example: Get Manager Details
```javascript
import axios from 'axios';

const getManagerDetails = async (managerId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/spa-managers/${managerId}/`
    );
    console.log('Manager details:', response.data);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

---

### Example: Download Document
```javascript
import axios from 'axios';

const downloadDocument = async (documentId) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/spa-manager-documents/${documentId}/download/`,
      {
        responseType: 'blob', // Important for file downloads
      }
    );
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'document.pdf');
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error:', error.response.data);
  }
};
```

---

## Testing in Django Admin

### Access Admin Panel:
```
http://localhost:8000/admin/
```

### Available Admin Sections:
1. **Spas → Spa Managers**
   - Create, view, edit, delete managers
   - Search by name, email, phone, spa
   - Filter by spa, created date

2. **Documents → Spa Manager Documents**
   - Upload, view, edit, delete documents
   - Search by title, manager name, notes
   - Filter by manager, uploader, date

---

## Postman Collection

### Import this JSON to Postman:

```json
{
  "info": {
    "name": "Spa Manager API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Spa Manager",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"fullname\": \"John Doe\",\n  \"email\": \"john@example.com\",\n  \"phone\": \"+1234567890\",\n  \"spa\": 1\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "http://localhost:8000/api/spa-managers/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "spa-managers", ""]
        }
      }
    },
    {
      "name": "List Spa Managers",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/api/spa-managers/",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "spa-managers", ""]
        }
      }
    }
  ]
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "spa_manager": ["This field is required."]
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
Check server logs for details.

---

## Notes

- **Authentication:** Currently set to `AllowAny` for documents, `IsAuthenticatedOrReadOnly` for managers
- **File Upload:** Use `multipart/form-data` content type
- **Pagination:** Default page size can be configured in settings
- **CORS:** Ensure CORS is properly configured for frontend access

---

## Happy Testing! 🎉

All endpoints are ready for integration with your frontend application!

