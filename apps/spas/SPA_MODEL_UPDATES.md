# Spa Model Updates - Primary & Secondary Owners + Agreement Status

## ✅ Changes Implemented

### 1. **Dual Owner Support** ✅

**Added Fields:**
- `primary_owner` (ForeignKey) - Main/Primary spa owner (required)
- `secondary_owner` (ForeignKey) - Secondary/Sub owner (optional)
- `sub_owners` (ManyToMany) - Multiple additional managers (optional)
- `owner` (ForeignKey) - Legacy field for backward compatibility

**Model Structure:**
```python
class Spa(models.Model):
    # Primary owner (required)
    primary_owner = models.ForeignKey(
        'SpaOwner', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='primary_spas',
        help_text="Primary Owner"
    )
    
    # Secondary owner (optional)
    secondary_owner = models.ForeignKey(
        'SpaOwner', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='secondary_spas',
        help_text="Secondary Owner / Sub Owner"
    )
    
    # Additional sub-owners/managers (optional)
    sub_owners = models.ManyToManyField(
        'SpaOwner', 
        blank=True, 
        related_name='managed_spas'
    )
```

---

### 2. **Agreement Status Updated** ✅

**Before:**
```python
AGREEMENT = [
    ('Active', 'Active'),
    ('Expired', 'Expired'),
    ('Not Avail', 'Not Avail')
]
```

**After:**
```python
AGREEMENT_STATUS_CHOICES = [
    ('done', 'Done'),
    ('pending', 'Pending'),
    ('expired', 'Expired')
]
agreement_status = models.CharField(
    max_length=50, 
    choices=AGREEMENT_STATUS_CHOICES, 
    default='pending'
)
```

---

### 3. **Enhanced Serializers** ✅

#### SpaListSerializer
```python
fields = [
    'id', 'spa_code', 'spa_name', 
    'primary_owner', 'primary_owner_name',      # ← New
    'secondary_owner', 'secondary_owner_name',  # ← New
    'status', 'agreement_status', 'agreement_status_display',
    'state', 'city', 'area', 'area_name', 'created_at'
]
```

#### SpaDetailSerializer
```python
fields = [
    'id', 'spa_code', 'spa_name', 
    'primary_owner', 'secondary_owner', 'sub_owners',  # ← All owners
    'opening_date', 'reopen_date', 
    'status', 'status_display',
    'line_track', 'landmark',
    'emails', 'phones', 'address', 
    'agreement_status', 'agreement_status_display', 'remark',
    'area', 'created_at', 'created_by'
]
```

#### SpaCreateUpdateSerializer
```python
fields = [
    'spa_code', 'spa_name', 
    'primary_owner', 'secondary_owner', 'sub_owners',  # ← All owners
    'opening_date', 'reopen_date',
    'status', 'line_track', 'landmark', 
    'emails', 'phones', 'address',
    'agreement_status', 'remark', 'area'
]

# Validation: Primary owner is required
def validate(self, data):
    if not data.get('primary_owner'):
        raise serializers.ValidationError({
            'primary_owner': 'Primary owner is required'
        })
    return data
```

---

### 4. **Advanced Filtering** ✅

**Created:** `apps/spas/filters.py`

**Available Filters:**
```python
# Text search
spa_name            # Contains (case-insensitive)
spa_code            # Contains (case-insensitive)

# Status filters
status              # Exact match (Open, Closed, Temporarily Closed)
agreement_status    # Exact match (done, pending, expired)

# Owner filters
primary_owner       # Filter by primary owner ID
secondary_owner     # Filter by secondary owner ID

# Location filters
state               # Filter by state ID
city                # Filter by city ID
area                # Filter by area ID

# Date range filters
opening_date_from   # Opening date >= date
opening_date_to     # Opening date <= date
created_from        # Created at >= datetime
created_to          # Created at <= datetime
```

**Usage Examples:**
```
GET /api/spas/?agreement_status=pending
GET /api/spas/?primary_owner=1
GET /api/spas/?status=Open&agreement_status=done
GET /api/spas/?state=1&city=2
GET /api/spas/?opening_date_from=2024-01-01&opening_date_to=2024-12-31
```

---

### 5. **Additional API Endpoints** ✅

#### Get Spas by Status
```
GET /api/spas/by_status/?status=Open
```

#### Get Spas by Agreement
```
GET /api/spas/by_agreement/?agreement_status=pending
```

#### Get Statistics
```
GET /api/spas/statistics/

Response:
{
  "total": 50,
  "by_status": {
    "Open": 30,
    "Closed": 15,
    "Temporarily Closed": 5
  },
  "by_agreement": {
    "done": 25,
    "pending": 15,
    "expired": 10
  },
  "with_primary_owner": 50,
  "with_secondary_owner": 30
}
```

#### Get Primary Owners Only
```
GET /api/spa-owners/primary_owners/
```

#### Get Sub Owners Only
```
GET /api/spa-owners/sub_owners/
```

---

### 6. **Updated Admin Panel** ✅

**List Display:**
- Spa Name
- Spa Code
- Primary Owner
- Secondary Owner
- Status
- Agreement Status
- Area
- Created At

**List Filters:**
- Status
- Agreement Status
- State → City → Area
- Primary Owner
- Secondary Owner

**Search Fields:**
- Spa Name
- Spa Code
- Primary Owner Name
- Secondary Owner Name
- Emails
- Phones

**Fieldsets:**
1. Basic Information
2. Ownership (Primary, Secondary, Sub-owners, Legacy)
3. Location
4. Contact Information
5. Important Dates
6. Agreement Details
7. Metadata (collapsible)

---

## Migration Applied ✅

**Migration:** `0002_spa_primary_owner_spa_secondary_owner_and_more.py`

**Changes:**
- ✅ Added `primary_owner` field
- ✅ Added `secondary_owner` field
- ✅ Updated `agreement_status` choices
- ✅ Updated `owner` field (legacy)

**Applied Successfully!**

---

## API Examples

### Create Spa with Both Owners

```bash
curl -X POST http://localhost:8000/api/spas/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "spa_code": "SPA001",
    "spa_name": "Luxury Spa Center",
    "primary_owner": 1,
    "secondary_owner": 2,
    "status": "Open",
    "agreement_status": "done",
    "area": 1,
    "emails": "spa@example.com, info@example.com",
    "phones": "+1234567890, +0987654321",
    "address": "123 Main Street",
    "opening_date": "2025-01-01"
  }'
```

### Get Spas with Filtering

```bash
# Get all pending agreement spas
GET /api/spas/?agreement_status=pending

# Get spas by primary owner
GET /api/spas/?primary_owner=1

# Get open spas with done agreements
GET /api/spas/?status=Open&agreement_status=done

# Search by spa name
GET /api/spas/?search=Luxury

# Filter by location
GET /api/spas/?state=1&city=2&area=3
```

### Response Example

```json
{
  "id": 1,
  "spa_code": "SPA001",
  "spa_name": "Luxury Spa Center",
  "primary_owner": {
    "id": 1,
    "fullname": "John Doe",
    "parent_owner": null,
    "parent_owner_name": null
  },
  "secondary_owner": {
    "id": 2,
    "fullname": "Jane Smith",
    "parent_owner": 1,
    "parent_owner_name": "John Doe"
  },
  "sub_owners": [],
  "status": "Open",
  "status_display": "Open",
  "agreement_status": "done",
  "agreement_status_display": "Done",
  "area": {
    "id": 1,
    "name": "Downtown",
    "city": {
      "id": 1,
      "name": "New York",
      "state": {
        "id": 1,
        "name": "New York"
      }
    }
  },
  "opening_date": "2025-01-01",
  "reopen_date": null,
  "emails": "spa@example.com, info@example.com",
  "phones": "+1234567890, +0987654321",
  "address": "123 Main Street",
  "line_track": null,
  "landmark": "Near Central Park",
  "remark": "Premium spa location",
  "created_at": "2025-10-08T10:00:00Z",
  "created_by": 1
}
```

---

## Backward Compatibility ✅

The `owner` field is kept as a legacy field:
- Auto-syncs with `primary_owner` on save
- Existing code still works
- Can be deprecated later

---

## Database Schema

```sql
CREATE TABLE spas (
    id INTEGER PRIMARY KEY,
    spa_code VARCHAR(50) UNIQUE,
    spa_name VARCHAR(200),
    
    -- Owners
    primary_owner_id INTEGER REFERENCES spa_owners(id),
    secondary_owner_id INTEGER REFERENCES spa_owners(id),
    owner_id INTEGER REFERENCES spa_owners(id),  -- Legacy
    
    -- Status
    status VARCHAR(30) DEFAULT 'Open',
    agreement_status VARCHAR(50) DEFAULT 'pending',
    
    -- Location
    area_id INTEGER REFERENCES areas(id),
    line_track VARCHAR(100),
    landmark VARCHAR(200),
    address TEXT,
    
    -- Contacts
    emails TEXT,
    phones TEXT,
    
    -- Dates
    opening_date DATE,
    reopen_date DATE,
    
    -- Other
    remark TEXT,
    created_at TIMESTAMP,
    created_by_id INTEGER REFERENCES users(id)
);

CREATE TABLE spas_sub_owners (
    id INTEGER PRIMARY KEY,
    spa_id INTEGER REFERENCES spas(id),
    spaowner_id INTEGER REFERENCES spa_owners(id)
);
```

---

## Admin Panel Features

### Creating a Spa:
1. **Basic Information**
   - Spa Code (unique)
   - Spa Name
   - Status (Open/Closed/Temporarily Closed)

2. **Ownership** (Required Section)
   - ✅ Primary Owner (required)
   - ✅ Secondary Owner (optional)
   - Sub-owners (optional, multiple)
   - Legacy owner (auto-filled)

3. **Location**
   - Area selection
   - Line track
   - Landmark
   - Full address

4. **Contact Information**
   - Emails (comma-separated)
   - Phones (comma-separated)

5. **Important Dates**
   - Opening Date
   - Reopen Date

6. **Agreement Details**
   - ✅ Status: Done / Pending / Expired
   - Remark

---

## Frontend Integration Requirements

### Update Spa Form Components

**Fields to Include:**

```javascript
{
  spa_code: string,
  spa_name: string,
  
  // Owners (BOTH visible in form)
  primary_owner: number,      // ← Required dropdown
  secondary_owner: number,    // ← Optional dropdown
  sub_owners: number[],       // ← Optional multi-select
  
  // Status
  status: 'Open' | 'Closed' | 'Temporarily Closed',
  agreement_status: 'done' | 'pending' | 'expired',  // ← Updated
  
  // Location
  area: number,
  line_track: string,
  landmark: string,
  address: string,
  
  // Contacts
  emails: string,             // Comma-separated
  phones: string,             // Comma-separated
  
  // Dates
  opening_date: string,       // YYYY-MM-DD
  reopen_date: string,        // YYYY-MM-DD
  
  // Other
  remark: string
}
```

### Agreement Status Options:
```javascript
const agreementOptions = [
  { value: 'done', label: 'Done' },
  { value: 'pending', label: 'Pending' },
  { value: 'expired', label: 'Expired' }
];
```

### Form Layout Example:
```jsx
{/* Ownership Section */}
<div className="grid grid-cols-2 gap-4">
  <div>
    <label>Primary Owner *</label>
    <select name="primary_owner" required>
      <option value="">Select Primary Owner</option>
      {owners.map(owner => (
        <option key={owner.id} value={owner.id}>
          {owner.fullname}
        </option>
      ))}
    </select>
  </div>
  
  <div>
    <label>Secondary Owner</label>
    <select name="secondary_owner">
      <option value="">Select Secondary Owner (Optional)</option>
      {owners.map(owner => (
        <option key={owner.id} value={owner.id}>
          {owner.fullname}
        </option>
      ))}
    </select>
  </div>
</div>

{/* Agreement Status */}
<div>
  <label>Agreement Status *</label>
  <select name="agreement_status" required>
    <option value="pending">Pending</option>
    <option value="done">Done</option>
    <option value="expired">Expired</option>
  </select>
</div>
```

---

## Filter Options for Frontend

### Status Filters:
```javascript
// Spa Status
['all', 'Open', 'Closed', 'Temporarily Closed']

// Agreement Status
['all', 'done', 'pending', 'expired']
```

### Display in Table:
```jsx
// Primary Owner Column
<td>{spa.primary_owner_name || '-'}</td>

// Secondary Owner Column
<td>{spa.secondary_owner_name || '-'}</td>

// Agreement Status Badge
<td>
  <span className={`badge ${getAgreementColor(spa.agreement_status)}`}>
    {spa.agreement_status_display}
  </span>
</td>
```

### Badge Colors:
```javascript
const getAgreementColor = (status) => {
  const colors = {
    'done': 'bg-green-500 text-white',
    'pending': 'bg-yellow-500 text-white',
    'expired': 'bg-red-500 text-white'
  };
  return colors[status] || 'bg-gray-500';
};
```

---

## Database Migration

**Migration File:** `apps/spas/migrations/0002_spa_primary_owner_spa_secondary_owner_and_more.py`

**Changes:**
- ✅ Added `primary_owner` field
- ✅ Added `secondary_owner` field
- ✅ Updated `agreement_status` choices (done, pending, expired)
- ✅ Modified `owner` field (legacy support)

**Status:** ✅ **Applied Successfully!**

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/spas/` | GET | List all spas with filters |
| `/api/spas/` | POST | Create new spa |
| `/api/spas/{id}/` | GET | Get spa details |
| `/api/spas/{id}/` | PATCH | Update spa |
| `/api/spas/{id}/` | DELETE | Delete spa |
| `/api/spas/statistics/` | GET | Get spa statistics |
| `/api/spas/by_status/?status=Open` | GET | Filter by status |
| `/api/spas/by_agreement/?agreement_status=done` | GET | Filter by agreement |
| `/api/spa-owners/` | GET | List all owners |
| `/api/spa-owners/primary_owners/` | GET | List primary owners only |
| `/api/spa-owners/sub_owners/` | GET | List sub owners only |

---

## Testing the Changes

### 1. Create Spa with Both Owners

```python
# Python Shell
from apps.spas.models import Spa, SpaOwner
from apps.location.models import Area

# Get or create owners
primary = SpaOwner.objects.create(fullname="John Doe")
secondary = SpaOwner.objects.create(fullname="Jane Smith", parent_owner=primary)

# Get area
area = Area.objects.first()

# Create spa
spa = Spa.objects.create(
    spa_code="SPA001",
    spa_name="Luxury Spa",
    primary_owner=primary,
    secondary_owner=secondary,
    area=area,
    status="Open",
    agreement_status="done"
)

print(f"Created: {spa}")
print(f"Primary: {spa.primary_owner}")
print(f"Secondary: {spa.secondary_owner}")
print(f"Agreement: {spa.get_agreement_status_display()}")
```

### 2. Test API

```bash
# Get all spas
curl http://localhost:8000/api/spas/

# Filter by agreement status
curl http://localhost:8000/api/spas/?agreement_status=pending

# Filter by primary owner
curl http://localhost:8000/api/spas/?primary_owner=1

# Get statistics
curl http://localhost:8000/api/spas/statistics/
```

---

## Admin Panel Usage

### Creating a Spa:

1. Go to **Admin Panel** → **Spas** → **Add Spa**

2. **Basic Information:**
   - Spa Code: `SPA001`
   - Spa Name: `Luxury Spa Center`
   - Status: `Open`

3. **Ownership:** ✅
   - Primary Owner: Select from dropdown (required)
   - Secondary Owner: Select from dropdown (optional)
   - Sub-owners: Select multiple (optional)

4. **Location:**
   - Area: Select area
   - Line Track, Landmark, Address

5. **Contact Information:**
   - Emails: `spa@example.com, info@example.com`
   - Phones: `+1234567890, +0987654321`

6. **Agreement Details:** ✅
   - Agreement Status: `Done` / `Pending` / `Expired`
   - Remark: Notes about agreement

7. **Save**

---

## Visual Changes

### Before:
```
Spa List:
┌──────────────┬──────────┬────────────┬────────┐
│ Name         │ Code     │ Owner      │ Status │
├──────────────┼──────────┼────────────┼────────┤
│ Luxury Spa   │ SPA001   │ John Doe   │ Open   │
└──────────────┴──────────┴────────────┴────────┘

Agreement: Active / Expired / Not Avail
```

### After:
```
Spa List:
┌──────────────┬──────────┬──────────────┬──────────────┬────────┬───────────┐
│ Name         │ Code     │ Primary      │ Secondary    │ Status │ Agreement │
├──────────────┼──────────┼──────────────┼──────────────┼────────┼───────────┤
│ Luxury Spa   │ SPA001   │ John Doe     │ Jane Smith   │ Open   │ Done      │
└──────────────┴──────────┴──────────────┴──────────────┴────────┴───────────┘

Agreement: Done / Pending / Expired
```

---

## Summary of Changes

### Models ✅
- Added `primary_owner` field
- Added `secondary_owner` field
- Updated agreement status choices
- Added auto-sync for legacy `owner` field

### Serializers ✅
- Include both primary and secondary owners
- Show owner names in list view
- Include agreement_status_display
- Validate primary owner is required

### Views ✅
- Updated queryset to include new fields
- Added custom filter endpoints
- Added statistics endpoint
- Better search and filtering

### Admin ✅
- Show both owners in list display
- Filter by both owners
- Search by both owners
- Clear fieldset organization
- Helpful descriptions

### Filters ✅
- Created comprehensive filter class
- Support for all fields
- Date range filtering
- Owner filtering

---

## Validation Rules

### Required Fields:
- ✅ `spa_code` (unique)
- ✅ `spa_name`
- ✅ `primary_owner`

### Optional Fields:
- `secondary_owner`
- `sub_owners`
- `area`
- All other fields

### Default Values:
- `status`: 'Open'
- `agreement_status`: 'pending'

---

## Next Steps

### For Frontend:
1. Update Spa form to include both owner dropdowns
2. Add agreement status dropdown with new options
3. Update table to show both owners
4. Add filtering UI for agreement status
5. Display both owners in detail view

### Files to Update:
- `frontend/Dashboard/admindashbboard/src/pages/Spas.jsx`
- `frontend/Dashboard/admindashbboard/src/components/Files/Spas/*`

---

## Status

✅ **Backend: COMPLETE**
- Models updated
- Migrations applied
- Serializers updated
- Views enhanced
- Admin panel configured
- Filters created
- API endpoints ready

🔄 **Frontend: PENDING**
- Need to update form components
- Need to update table display
- Need to add filter options

---

## Benefits

1. **Clear Ownership Structure**
   - Primary owner clearly identified
   - Secondary owner optional but visible
   - Multiple sub-owners supported

2. **Better Agreement Tracking**
   - Clear status: Done, Pending, Expired
   - Easy to filter and report
   - More meaningful than Active/Not Avail

3. **Enhanced Filtering**
   - Filter by either owner
   - Filter by agreement status
   - Combine multiple filters
   - Date range support

4. **Improved Admin Experience**
   - Both owners in list view
   - Better organized fieldsets
   - Helpful field descriptions
   - Better search capabilities

**All backend changes complete and tested!** 🎉

