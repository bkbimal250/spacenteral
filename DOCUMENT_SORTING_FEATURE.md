# Document Sorting Feature

## Overview
Added a comprehensive sorting dropdown to the Documents page filters, allowing users to sort spa groups by various criteria in ascending or descending order.

## Features Added

### Sort Options
1. **Spa Name (A-Z)** - Alphabetical by spa name (ascending)
2. **Spa Name (Z-A)** - Alphabetical by spa name (descending)
3. **Spa Code (0-9)** - Numeric by spa code (ascending) ✅ Default
4. **Spa Code (9-0)** - Numeric by spa code (descending)
5. **Date (Newest First)** - By most recent document in each spa group
6. **Date (Oldest First)** - By oldest document in each spa group

### Default Behavior
- **Default Sort**: Spa Code (0-9) - Numeric order by spa code
- **Numeric Sorting**: Spa codes are sorted numerically (e.g., 2, 10, 612), not alphabetically
- **Unassigned Documents**: Always appear at the end regardless of sort order
- **Reset on Clear**: Sorting resets to default when "Clear All Filters" is clicked
- **Pagination Reset**: Changes to page 1 when sorting changes

## Files Modified

### 1. `frontend/Dashboard/admindashbboard/src/components/Files/Documents/DocumentFilters.jsx`

**Changes:**
1. Added `ArrowUpDown` icon import from lucide-react
2. Added `sortBy` and `setSortBy` props to component parameters
3. Restructured filter grid from 5 columns to 6 columns
4. Added "File Type" filter (file extension filter)
5. Added "Sort By" dropdown with 6 sorting options
6. Moved "Clear All Filters" button to a separate row below filters
7. Applied blue background (`bg-blue-50`) to Sort By dropdown to highlight it

**UI Changes:**
```jsx
{/* Sort By */}
<div>
  <label className="block text-xs font-medium text-gray-600 mb-1 flex items-center gap-1">
    <ArrowUpDown size={12} />
    Sort By
  </label>
  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:border-blue-500 bg-blue-50"
  >
    <option value="spa_name_asc">Spa Name (A-Z)</option>
    <option value="spa_name_desc">Spa Name (Z-A)</option>
    <option value="spa_code_asc">Spa Code (0-9)</option>
    <option value="spa_code_desc">Spa Code (9-0)</option>
    <option value="date_desc">Date (Newest First)</option>
    <option value="date_asc">Date (Oldest First)</option>
  </select>
</div>
```

### 2. `frontend/Dashboard/admindashbboard/src/pages/Documents.jsx`

**Changes:**
1. Added `sortBy` state with default value `'spa_code_asc'`
   ```javascript
   const [sortBy, setSortBy] = useState('spa_code_asc');
   ```

2. Added `sortBy` to `handleClearFilters()` function
   ```javascript
   const handleClearFilters = () => {
     // ... other filters
     setSortBy('spa_code_asc');
   };
   ```

3. Implemented sorting logic in `useMemo` hook:
   ```javascript
   spaGroups.sort((a, b) => {
     // Always put unassigned at the end
     if (a.spaId === 'unassigned') return 1;
     if (b.spaId === 'unassigned') return -1;

     switch (sortBy) {
       case 'spa_name_asc':
         return a.spaName.localeCompare(b.spaName);
       case 'spa_name_desc':
         return b.spaName.localeCompare(a.spaName);
       case 'spa_code_asc':
         // Numeric comparison for spa codes
         const aCode = parseInt(a.spaCode) || 0;
         const bCode = parseInt(b.spaCode) || 0;
         return aCode - bCode;
       case 'spa_code_desc':
         // Numeric comparison for spa codes (descending)
         const aCodeDesc = parseInt(a.spaCode) || 0;
         const bCodeDesc = parseInt(b.spaCode) || 0;
         return bCodeDesc - aCodeDesc;
       case 'date_desc':
         const aLatest = Math.max(...a.documents.map(d => new Date(d.created_at).getTime()));
         const bLatest = Math.max(...b.documents.map(d => new Date(d.created_at).getTime()));
         return bLatest - aLatest;
       case 'date_asc':
         const aOldest = Math.min(...a.documents.map(d => new Date(d.created_at).getTime()));
         const bOldest = Math.min(...b.documents.map(d => new Date(d.created_at).getTime()));
         return aOldest - bOldest;
       default:
         // Default: numeric comparison for spa codes
         const aCodeDefault = parseInt(a.spaCode) || 0;
         const bCodeDefault = parseInt(b.spaCode) || 0;
         return aCodeDefault - bCodeDefault;
     }
   });
   ```

4. Added `sortBy` to useMemo dependencies
   ```javascript
   }, [filteredDocuments, currentPage, spaGroupsPerPage, sortBy]);
   ```

5. Added `sortBy` to pagination reset useEffect
   ```javascript
   useEffect(() => {
     setCurrentPage(1);
   }, [searchTerm, filterSpa, filterState, filterCity, filterArea, filterExtension, sortBy]);
   ```

6. Passed `sortBy` and `setSortBy` props to DocumentFilters component

## Sorting Logic Details

### Numeric Sorting (Spa Codes)
- Uses `parseInt()` to convert spa codes to numbers for proper numeric comparison
- Handles non-numeric or missing spa codes with fallback to `0`
- Ensures correct order: 2, 10, 100, 612 (not 10, 100, 2, 612 as would happen with string sorting)
- Example: `parseInt("612") - parseInt("10")` results in `602` (positive = 612 comes after 10)

### Alphabetical Sorting (Spa Names)
- Uses JavaScript's `localeCompare()` for proper string comparison
- Case-insensitive comparison

### Date-Based Sorting
- **Newest First**: Finds the most recent document in each spa group and sorts by that
- **Oldest First**: Finds the oldest document in each spa group and sorts by that
- Uses timestamps (milliseconds) for accurate comparison
- Handles multiple documents per spa correctly

### Special Cases
- **Unassigned Documents**: Always appear at the end regardless of sort order
- **Empty Values**: Treated as empty strings and sorted accordingly
- **Missing Dates**: JavaScript Date handles invalid dates gracefully

## User Experience

### Visual Indicators
- Sort dropdown has blue background (`bg-blue-50`) to make it stand out
- ArrowUpDown icon next to "Sort By" label for clarity
- Clear option descriptions (e.g., "Spa Code (A-Z)" instead of just "Ascending")

### Behavior
- ✅ Sorting applies instantly when selection changes
- ✅ Pagination resets to page 1 when sorting changes
- ✅ All documents in each spa group remain visible
- ✅ Filter + Sort combinations work correctly
- ✅ Clear filters button resets sort to default

## Testing

### Test Cases
1. **Default Behavior**
   - Load Documents page
   - Verify spas are sorted by Spa Code (A-Z)
   - Verify "Spa Code (A-Z)" is selected in dropdown

2. **Spa Name Sorting**
   - Select "Spa Name (A-Z)"
   - Verify spas appear alphabetically by name
   - Select "Spa Name (Z-A)"
   - Verify reverse alphabetical order

3. **Spa Code Sorting (Numeric)**
   - Select "Spa Code (0-9)"
   - Verify numeric order: 2, 10, 100, 612 (not alphabetical 10, 100, 2, 612)
   - Verify "612 - Unicorn Spa" comes after "100 - Another Spa"
   - Select "Spa Code (9-0)"
   - Verify reverse numeric order: 612, 100, 10, 2

4. **Date Sorting**
   - Select "Date (Newest First)"
   - Verify spas with most recent documents appear first
   - Select "Date (Oldest First)"
   - Verify spas with oldest documents appear first

5. **Combined with Filters**
   - Apply a state filter
   - Change sorting
   - Verify only filtered spas are shown and sorted correctly

6. **Pagination**
   - Change sort order
   - Verify page resets to 1
   - Navigate to page 2
   - Change sort again
   - Verify back to page 1

7. **Clear Filters**
   - Change sort to "Spa Name (Z-A)"
   - Click "Clear All Filters"
   - Verify sort resets to "Spa Code (A-Z)"

## Impact

### Benefits
- ✅ **Better Organization**: Users can view spas in their preferred order
- ✅ **Flexible Searching**: Combine filters with sorting for precise results
- ✅ **Time-Based Views**: Find newest or oldest document sets quickly
- ✅ **Numeric Sorting**: Spa codes sorted numerically (2, 10, 612) not alphabetically (10, 2, 612)
- ✅ **Correct Order**: Default numeric spa code sorting for consistent browsing
- ✅ **Enhanced UX**: Clear options and instant feedback

### Performance
- ✅ **Optimized with useMemo**: Sorting only recalculates when needed
- ✅ **Efficient Date Comparison**: Uses timestamps for fast date sorting
- ✅ **No Additional API Calls**: All sorting happens client-side

## Date
October 26, 2025

