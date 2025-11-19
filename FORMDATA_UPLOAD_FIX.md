# FormData Upload Fix - 400 Error Resolution

## Issue Description
Users were getting a **400 Bad Request** error when trying to upload documents in the admin dashboard's SpaView.jsx. The error showed that the `data` object in the request was empty `{}`, meaning the FormData wasn't being sent properly to the backend.

## Root Cause
The issue was caused by explicitly setting `Content-Type: multipart/form-data` in the axios request headers. When uploading files with FormData, the browser needs to automatically set the Content-Type header with the correct **boundary parameter**, which looks like this:

```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
```

By explicitly setting `Content-Type: multipart/form-data` without the boundary parameter, the backend couldn't properly parse the multipart data, resulting in an empty request body and a 400 error.

## Solution
Set `Content-Type: undefined` for all FormData uploads. This allows the browser to automatically set the correct Content-Type header with the boundary parameter.

### Changes Made

#### Admin Dashboard
**File:** `frontend/Dashboard/admindashbboard/src/services/documentService.js`

1. **createDocument** (Line 22-29)
   ```javascript
   createDocument: async (formData) => {
     const response = await api.post('/documents/', formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

2. **updateDocument** (Line 31-38)
   ```javascript
   updateDocument: async (id, formData) => {
     const response = await api.patch(`/documents/${id}/`, formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

3. **createOwnerDocument** (Line 90-97)
   ```javascript
   createOwnerDocument: async (formData) => {
     const response = await api.post('/owner-documents/', formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

4. **updateOwnerDocument** (Line 99-106)
   ```javascript
   updateOwnerDocument: async (id, formData) => {
     const response = await api.patch(`/owner-documents/${id}/`, formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

5. **createSpaManagerDocument** (Line 148-155)
   ```javascript
   createSpaManagerDocument: async (formData) => {
     const response = await api.post('/spa-manager-documents/', formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

6. **updateSpaManagerDocument** (Line 157-164)
   ```javascript
   updateSpaManagerDocument: async (id, formData) => {
     const response = await api.patch(`/spa-manager-documents/${id}/`, formData, {
       headers: {
         'Content-Type': undefined, // Let browser set it with boundary
       },
     });
     return response.data;
   },
   ```

#### Manager Dashboard
**File:** `frontend/Dashboard/managerdashboard/src/services/documentService.js`

1. **createDocument** (Line 22-29)
2. **updateDocument** (Line 31-38)

All updated with the same fix: `'Content-Type': undefined`

## Technical Explanation

### Before (Incorrect)
```javascript
await api.post('/documents/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data', // ❌ Missing boundary!
  },
});
```

**Request Header:**
```
Content-Type: multipart/form-data
```

**Problem:** No boundary parameter, backend can't parse the multipart sections.

### After (Correct)
```javascript
await api.post('/documents/', formData, {
  headers: {
    'Content-Type': undefined, // ✅ Browser sets it automatically
  },
});
```

**Request Header (set by browser):**
```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
```

**Result:** Backend can properly parse all form fields and files.

## Why This Works

1. **FormData Object**: When you create a FormData object and append data to it, the browser knows it needs to send multipart/form-data.

2. **Boundary Parameter**: The browser generates a unique boundary string that separates different parts of the multipart data.

3. **Automatic Header**: When Content-Type is `undefined`, axios removes it from the request, allowing the browser to set the complete header with the boundary.

4. **Backend Parsing**: The backend uses the boundary parameter to correctly parse each section of the multipart data (title, doc_type, spa, file, notes).

## Error Before Fix

```json
{
  "message": "Request failed with status code 400",
  "code": "ERR_BAD_REQUEST",
  "status": 400,
  "data": {} // ❌ Empty! FormData not sent properly
}
```

## Result After Fix

```javascript
// FormData properly sent with:
{
  title: "Document Title",
  doc_type: 1,
  spa: 123,
  file: File object,
  notes: "Optional notes"
}
// ✅ All fields received by backend
// ✅ Document uploaded successfully
```

## Files Modified

| File | Changes | Lines |
|------|---------|-------|
| `documentService.js` (Admin) | Fixed 6 FormData methods | 22-164 |
| `documentService.js` (Manager) | Fixed 2 FormData methods | 22-38 |

## Testing

### Before Fix
1. ✅ Select file in SpaView
2. ✅ Fill form fields
3. ✅ Click upload
4. ❌ **400 Error** - "Request failed with status code 400"
5. ❌ Data object empty in request

### After Fix
1. ✅ Select file in SpaView
2. ✅ Fill form fields
3. ✅ Click upload
4. ✅ **Success!** - "Document uploaded successfully!"
5. ✅ All FormData fields sent correctly
6. ✅ File uploaded to backend

## Related Issues Fixed

This fix resolves upload errors in:
- ✅ Spa documents upload (SpaView.jsx)
- ✅ Manager documents upload (SpaView.jsx)
- ✅ Owner documents upload (Documents page)
- ✅ All document update operations
- ✅ Both admin and manager dashboards

## Best Practice

**When uploading files with FormData in axios:**
- ✅ Set `'Content-Type': undefined`
- ✅ Let the browser handle the boundary parameter
- ❌ Don't manually set `'Content-Type': 'multipart/form-data'`
- ❌ Don't set Content-Type at all for FormData

## Backend Validation Fix

After fixing the FormData issue, there was still a **30MB validation error** coming from the backend. Fixed by updating:

**File:** `apps/documents/validators.py`
- **Line 39-40:** Changed `MAX_FILE_SIZE` from 30MB to 500MB

```python
# Before
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB in bytes

# After
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB in bytes
```

**File:** `spa_central/settings.py`
- **Line 190:** Updated comment to reflect 500MB limit
- **Lines 191-192:** Already set to 500MB

```python
# File Upload Settings (500MB max for documents and images)
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024  # 500MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024  # 500MB
```

## Additional Notes

- The axios instance in `api.js` has a default `Content-Type: application/json` header
- Setting `Content-Type: undefined` overrides this default
- This allows the browser's native FormData handling to work correctly
- The Authorization token is still sent correctly (handled by interceptor)
- Backend (Django) now fully configured to handle multipart/form-data (500MB limit)
- All validators, settings, and frontend now aligned at 500MB

