# Document Upload Fix - Manager Dashboard

## Issue Description
Users were unable to submit the document upload form in the manager dashboard, getting the error "Please select a spa". Additionally, the file size limit needed to be increased from 30MB to 500MB. The "Save & Add Another" button was also missing and needed to be implemented.

## Changes Made

### 1. **Increased File Size Limit to 500MB**

#### Frontend - Manager Dashboard
**File:** `frontend/Dashboard/managerdashboard/src/components/Files/Documents/DocumentForm.jsx`
- **Line 28-32:** Updated file size validation from 30MB to 500MB
- Changed `const maxSize = 10 * 1024 * 1024 * 3` to `const maxSize = 500 * 1024 * 1024`
- Updated error message from "File size must be less than 30MB" to "File size must be less than 500MB"

#### Backend Settings
**File:** `spa_central/settings.py`
- **Lines 191-192:** Already configured for 500MB
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024  # 500MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024  # 500MB
```

### 2. **Enhanced Form Validation and Debugging**

#### Frontend - Manager Dashboard
**File:** `frontend/Dashboard/managerdashboard/src/pages/Documents.jsx`
- **Lines 119-127:** Added comprehensive debugging logs
  - Logs form data before submission
  - Logs number of available spas
  - Enhanced spa validation to check for both falsy values and empty strings
- **Lines 130-134:** Added file validation for new uploads
- **Lines 149-153:** Added FormData logging to debug API submissions
- **Lines 165-172:** Enhanced error handling with detailed error response logging

### 3. **Implemented "Save & Add Another" Button**

#### Frontend - Manager Dashboard
**File:** `frontend/Dashboard/managerdashboard/src/components/Files/Documents/DocumentForm.jsx`
- **Lines 70-73:** Added `handleInternalSubmit` function to pass `addAnother` flag
- **Line 76:** Added click event handlers to prevent modal closing on outside clicks
- **Lines 224-232:** Added "Save & Add Another" button (shown only for new uploads, not edits)
  - Green button styled for visibility
  - Positioned between Cancel and Upload buttons

**File:** `frontend/Dashboard/managerdashboard/src/pages/Documents.jsx`
- **Line 116:** Updated `handleSubmit` to accept `addAnother` parameter
- **Lines 164-180:** Added logic to handle "Save & Add Another" functionality
  - Keeps modal open when `addAnother` is true
  - Resets form but keeps `doc_type` and `spa` selections
  - Clears title, file, and notes for next document
  - Scrolls modal to top for better UX

**File:** `frontend/Dashboard/managerdashboard/src/components/Files/Documents/DocumentModal.jsx`
- **Line 8:** Updated `handleSubmit` to pass `addAnother` parameter to parent
- **Lines 16-18:** Removed `onClick` from backdrop to prevent accidental closes
- **Line 22:** Added `modal-content` class for scroll targeting

## Technical Details

### File Size Limit
- **Frontend Validation:** 500MB (524,288,000 bytes)
- **Backend Limit:** 500MB for both `FILE_UPLOAD_MAX_MEMORY_SIZE` and `DATA_UPLOAD_MAX_MEMORY_SIZE`
- **Security:** File type validation still enforced via `ALLOWED_UPLOAD_EXTENSIONS`

### Validation Improvements
1. **Spa Selection:** Now validates `if (!formData.spa || formData.spa === '')`
2. **File Upload:** Ensures file is present for new uploads (not required for edits)
3. **Debug Console Logs:** Help identify where submission fails

### API Integration
- **Endpoint:** `/documents/` (POST for create, PATCH for update)
- **Content-Type:** `multipart/form-data`
- **Required Fields:** 
  - `title` (string)
  - `doc_type` (integer - document type ID)
  - `spa` (integer - spa ID)
  - `file` (file upload - required for new, optional for updates)
  - `notes` (string - optional)

## Testing Recommendations

1. **Test Spa Selection:**
   - Open browser console (F12)
   - Click "Upload" button in Documents page
   - Check console for "Spas available: X" log
   - If X is 0, verify spa service API is working

2. **Test File Upload:**
   - Select a file larger than 30MB but less than 500MB
   - Verify no file size error appears
   - Submit the form
   - Check console logs for FormData entries

3. **Test Form Submission:**
   - Fill all required fields (Title, Document Type, Spa, File)
   - Click Upload button
   - Check console for:
     - "Form Data:" log
     - "Sending FormData:" log with all field entries
   - Verify success toast message appears

4. **Test Error Scenarios:**
   - Try submitting without selecting a spa - should show "Please select a spa"
   - Try submitting without a file (new upload) - should show "Please select a file to upload"
   - Try uploading a file larger than 500MB - should show "File size must be less than 500MB"

## Related Files

### Modified Files
1. `frontend/Dashboard/managerdashboard/src/components/Files/Documents/DocumentForm.jsx` - File size limit, Save & Add Another button
2. `frontend/Dashboard/managerdashboard/src/pages/Documents.jsx` - Enhanced validation, Save & Add Another logic
3. `frontend/Dashboard/managerdashboard/src/components/Files/Documents/DocumentModal.jsx` - Pass addAnother parameter, prevent outside click close

### Verified Files (Already Correct)
1. `frontend/Dashboard/admindashbboard/src/components/Files/Documents/DocumentForm.jsx` - Already has 500MB limit and Save & Add Another
2. `spa_central/settings.py` - Already configured for 500MB

## Admin Dashboard Status
**Updated:** The admin dashboard SpaView.jsx has been updated to include 500MB file size validation for both spa documents and manager documents upload functionality.

### Admin Dashboard Changes (SpaView.jsx)
**File:** `frontend/Dashboard/admindashbboard/src/Detailview/SpaView.jsx`
- **Lines 185-197:** Added 500MB file size validation to `handleFileChange` (spa documents)
- **Lines 351-363:** Added 500MB file size validation to `handleManagerFileChange` (manager documents)
- **Lines 433-439:** Enhanced `formatFileSize` function to support GB display
- **Line 1116:** Updated manager upload form to use `formatFileSize` for better display
- **Line 1359:** Updated spa upload form to use `formatFileSize` for better display

## Next Steps
If the "Please select a spa" error persists after these changes:
1. Check browser console for the "Spas available" count
2. Verify the spa service API is returning data
3. Check if there are any CORS or authentication issues preventing spa data from loading
4. Verify the user has permission to access the spas endpoint

