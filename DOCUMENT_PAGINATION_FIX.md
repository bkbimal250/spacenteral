# Document Pagination Fix

## Issue
When viewing documents grouped by spa in the Documents page, only 5 documents were shown for "612 - Unicorn Spa (Arth Thai Spa)" instead of all 8 documents. The spa header correctly showed "8 Documents" but only 5 were visible in the grid below.

## Root Cause
The documents were being **paginated BEFORE grouping by spa**:
1. Fetch documents from API (30 documents default)
2. Filter documents → Get filtered results
3. **Paginate to 30 documents per page** ← Problem happens here
4. Group those 30 documents by spa
5. Display grouped documents

When paginating documents before grouping, if "Unicorn Spa" has 8 documents but 3 of them fall outside the 30-document window, only 5 documents would be visible in that spa's group.

## Solution
**Smart Spa-Group Pagination:**

The correct approach is to:
1. Fetch ALL documents from API with `page_size: 10000`
2. Filter documents based on search/filters
3. **Group documents by spa first**
4. **Paginate the spa groups** (show 30 spa groups per page)
5. Display paginated spa groups with ALL their documents

This ensures:
- ✅ Every spa group shows ALL its documents (all 8 for Unicorn Spa)
- ✅ Pagination still works (30 spa groups per page, not 30 documents)
- ✅ Better user experience - see complete information for each spa

## Files Modified

### 1. `frontend/Dashboard/admindashbboard/src/pages/Documents.jsx`

**Key Changes:**

1. **Import useMemo for memoization:**
   ```javascript
   import { useState, useEffect, useMemo } from 'react';
   ```

2. **Updated `fetchAllData()` to fetch all documents with `page_size: 10000`:**
   ```javascript
   documentService.getDocuments({ page_size: 10000 })
   documentService.getDocumentTypes({ page_size: 10000 })
   // ... and all other data sources
   ```

3. **Changed pagination state to track spa groups instead of documents:**
   ```javascript
   // Before: paginate documents
   const [currentPage, setCurrentPage] = useState(1);
   const itemsPerPage = 30;
   
   // After: paginate spa groups
   const [currentPage, setCurrentPage] = useState(1);
   const spaGroupsPerPage = 30;  // 30 spas per page, not 30 documents
   ```

4. **Added smart pagination logic with useMemo (Lines 227-267):**
   ```javascript
   const { paginatedDocuments, totalSpaGroups, totalDocuments } = useMemo(() => {
     // Step 1: Group documents by SPA
     const grouped = {};
     filteredDocuments.forEach(doc => {
       const spaId = doc.spa || 'unassigned';
       if (!grouped[spaId]) {
         grouped[spaId] = { spaId, spaName, spaCode, documents: [] };
       }
       grouped[spaId].documents.push(doc);
     });
   
     // Step 2: Convert to array and sort
     const spaGroups = Object.values(grouped).sort(...);
   
     // Step 3: Paginate SPA GROUPS (not documents)
     const startIndex = (currentPage - 1) * spaGroupsPerPage;
     const endIndex = startIndex + spaGroupsPerPage;
     const paginatedSpaGroups = spaGroups.slice(startIndex, endIndex);
   
     // Step 4: Flatten back to documents array
     const paginatedDocs = paginatedSpaGroups.flatMap(group => group.documents);
   
     return {
       paginatedDocuments: paginatedDocs,
       totalSpaGroups: spaGroups.length,
       totalDocuments: filteredDocuments.length
     };
   }, [filteredDocuments, currentPage, spaGroupsPerPage]);
   ```

5. **Updated Pagination to use spa group counts:**
   ```javascript
   <Pagination
     currentPage={currentPage}
     totalItems={totalSpaGroups}        // spa groups, not documents
     itemsPerPage={spaGroupsPerPage}    // 30 spa groups per page
     onPageChange={setCurrentPage}
   />
   ```

6. **Added informative pagination counter:**
   ```javascript
   <div className="mt-4 mb-2 text-center text-sm text-gray-600">
     Showing page {currentPage} of {Math.ceil(totalSpaGroups / spaGroupsPerPage)} 
     ({totalSpaGroups} spas, {totalDocuments} documents)
   </div>
   ```

### 2. `frontend/Dashboard/admindashbboard/src/Detailview/SpaView.jsx`
**Line 87**: Updated `fetchSpaDocuments()` function
```javascript
// Before
const data = await documentService.getDocuments({ spa: id });

// After
const data = await documentService.getDocuments({ spa: id, page_size: 10000 });
```

**Line 98**: Updated `fetchDocumentTypes()` function
```javascript
// Before
const data = await documentService.getDocumentTypes();

// After
const data = await documentService.getDocumentTypes({ page_size: 10000 });
```

### 3. `frontend/Dashboard/admindashbboard/src/Detailview/Ownerview.jsx`
**Line 59**: Updated `fetchOwnerDocuments()` function
```javascript
// Before
const params = {};

// After
const params = { page_size: 10000 };
```

### 4. `frontend/Dashboard/admindashbboard/src/Detailview/Managerview.jsx`
**Line 57**: Updated `fetchManagerDocuments()` function
```javascript
// Before
const data = await spaService.getSpaManagerDocuments({ spa_manager: id });

// After
const data = await spaService.getSpaManagerDocuments({ spa_manager: id, page_size: 10000 });
```

## Testing
After these changes:
1. Navigate to the Documents page (`/documents`)
2. Look at "612 - Unicorn Spa (Arth Thai Spa)" 
3. ✅ Verify the header shows "8 Documents"
4. ✅ Verify all 8 document cards are visible in the grid
5. Check pagination controls at the bottom
6. ✅ Verify it shows "30 spa groups per page"
7. Navigate to page 2 and back
8. ✅ Each spa on any page shows ALL its documents
9. Test filters/search
10. ✅ Pagination resets to page 1 when filters change
11. Check the info text: "Showing page X of Y (N spas, M documents)"

## Impact
- ✅ **Fixed**: All documents for each spa are now visible (8/8 for Unicorn Spa)
- ✅ **Smart Pagination**: Shows 30 spa groups per page (not 30 documents)
- ✅ **Complete Groups**: Each spa shows ALL its documents, not partial groups
- ✅ **Better Performance**: Uses useMemo for optimized re-renders
- ✅ **Clear Info**: Shows both spa count and document count in pagination
- ✅ **Filter Compatible**: Filters work correctly with spa-group pagination
- ✅ **User-Friendly**: Easier to browse spas with complete information

## Date
October 26, 2025

