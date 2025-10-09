# User Profile Update API - Complete Guide

## ✅ Backend Status: READY

The backend is **fully configured** for users to update their own profiles after admin creates their accounts.

## Available Endpoints

### 1. Get Current User Profile
**Endpoint:** `GET /api/users/me/`  
**Authentication:** Required (Token)  
**Permission:** Any authenticated user

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "employee",
  "phone": "+1234567890",
  "profile_picture": "/media/profile_pictures/user_1.jpg",
  "date_of_birth": "1990-01-01",
  "address": "123 Main St, City, State",
  "is_verified": true,
  "created_at": "2025-10-08T10:00:00Z",
  "updated_at": "2025-10-08T10:00:00Z",
  "profile": {
    "bio": "Software developer",
    "preferences": {},
    "notification_settings": {}
  }
}
```

---

### 2. Update Current User Profile
**Endpoint:** `PATCH /api/users/me/` or `PUT /api/users/me/`  
**Authentication:** Required (Token)  
**Permission:** Any authenticated user  
**Content-Type:** `multipart/form-data` (for profile picture)

**Allowed Fields:**
- `first_name` (string)
- `last_name` (string)
- `phone` (string)
- `profile_picture` (file upload)
- `date_of_birth` (date: YYYY-MM-DD)
- `address` (text)

**NOT Allowed (Admin Only):**
- ❌ `email` - Cannot change email
- ❌ `user_type` - Cannot change role
- ❌ `is_verified` - Admin only
- ❌ `is_active` - Admin only

**Example Request (using FormData):**
```javascript
const formData = new FormData();
formData.append('first_name', 'John');
formData.append('last_name', 'Doe');
formData.append('phone', '+1234567890');
formData.append('profile_picture', fileObject);
formData.append('date_of_birth', '1990-01-01');
formData.append('address', '123 Main St');

fetch('/api/users/me/', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Token YOUR_TOKEN'
  },
  body: formData
});
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "employee",
  "phone": "+1234567890",
  "profile_picture": "/media/profile_pictures/user_1_updated.jpg",
  "date_of_birth": "1990-01-01",
  "address": "123 Main St, City, State",
  ...
}
```

---

### 3. Change Password
**Endpoint:** `POST /api/users/change_password/`  
**Authentication:** Required (Token)  
**Permission:** Any authenticated user

**Request Body:**
```json
{
  "old_password": "current_password",
  "new_password": "new_password123",
  "new_password2": "new_password123"
}
```

**Validation:**
- Old password must be correct
- New password must meet requirements (8+ characters, etc.)
- New passwords must match

**Response (Success):**
```json
{
  "message": "Password updated successfully."
}
```

**Response (Error):**
```json
{
  "old_password": "Wrong password."
}
```

---

### 4. Get Extended Profile
**Endpoint:** `GET /api/profiles/my_profile/`  
**Authentication:** Required (Token)  
**Permission:** Any authenticated user

**Response:**
```json
{
  "bio": "Software developer with 5 years experience",
  "preferences": {
    "theme": "dark",
    "language": "en"
  },
  "notification_settings": {
    "email_notifications": true,
    "sms_notifications": false
  }
}
```

---

### 5. Update Extended Profile
**Endpoint:** `PATCH /api/profiles/my_profile/`  
**Authentication:** Required (Token)  
**Permission:** Any authenticated user

**Request Body:**
```json
{
  "bio": "Updated bio",
  "preferences": {
    "theme": "light"
  },
  "notification_settings": {
    "email_notifications": false
  }
}
```

---

## Security Features

### ✅ What Users CAN Do:
- Update their own name, phone, address
- Upload/change profile picture
- Update date of birth
- Change their password
- Update bio and preferences
- View their own profile

### ❌ What Users CANNOT Do:
- Change their email address
- Change their user role/type
- View or modify other users' profiles
- Access admin-only endpoints
- Change verification status
- Modify account creation date

---

## Frontend Integration

### Using the Profile Service

**File:** `frontend/Dashboard/admindashbboard/src/services/profileService.js`

```javascript
import profileService from '../services/profileService';

// Get current user profile
const profile = await profileService.getMyProfile();

// Update profile
const updated = await profileService.updateMyProfile({
  first_name: 'John',
  last_name: 'Doe',
  phone: '+1234567890',
  profile_picture: fileObject,  // File from input
  date_of_birth: '1990-01-01',
  address: '123 Main St'
});

// Change password
await profileService.changePassword(
  'old_password',
  'new_password',
  'new_password'
);

// Update extended profile
await profileService.updateExtendedProfile({
  bio: 'My bio',
  preferences: { theme: 'dark' }
});
```

---

## User Flow

### 1. Admin Creates User Account
```
Admin Dashboard → Users → Add User
- Email: user@example.com
- Password: temp_password
- First Name: John
- Last Name: Doe
- User Type: Employee
```

### 2. User Receives Credentials
```
Email: user@example.com
Password: temp_password
```

### 3. User Logs In
```
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "temp_password"
}

Response:
{
  "token": "abc123...",
  "user": { ... }
}
```

### 4. User Updates Profile (First Time)
```
User Dashboard → Profile Settings
- Change password (recommended)
- Upload profile picture
- Update phone number
- Add address
- Add date of birth
```

### 5. Ongoing Profile Management
```
Users can update their profile anytime:
- Change password regularly
- Update profile picture
- Modify contact information
- Update preferences
```

---

## Example Frontend Component

```jsx
import { useState, useEffect } from 'react';
import profileService from '../services/profileService';

const MyProfile = () => {
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    date_of_birth: '',
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    const data = await profileService.getMyProfile();
    setProfile(data);
    setFormData({
      first_name: data.first_name,
      last_name: data.last_name,
      phone: data.phone || '',
      address: data.address || '',
      date_of_birth: data.date_of_birth || '',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await profileService.updateMyProfile(formData);
      alert('Profile updated successfully!');
      loadProfile();
    } catch (error) {
      alert('Error updating profile');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={formData.first_name}
        onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
        placeholder="First Name"
      />
      {/* Add more fields */}
      <button type="submit">Update Profile</button>
    </form>
  );
};
```

---

## Testing

### Using cURL:

**1. Get Profile:**
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**2. Update Profile:**
```bash
curl -X PATCH http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "phone=+1234567890" \
  -F "profile_picture=@/path/to/image.jpg"
```

**3. Change Password:**
```bash
curl -X POST http://localhost:8000/api/users/change_password/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "old_pass",
    "new_password": "new_pass123",
    "new_password2": "new_pass123"
  }'
```

---

## Validation Rules

### Profile Picture:
- **Max Size:** 10MB (configurable in settings.py)
- **Formats:** JPG, JPEG, PNG, GIF
- **Storage:** Uploaded to `media/profile_pictures/`

### Phone:
- **Max Length:** 20 characters
- **Format:** Any (consider adding validation)

### Password:
- **Min Length:** 8 characters
- **Requirements:** Django's default validators
  - Not too similar to user information
  - Not entirely numeric
  - Not a common password

### Date of Birth:
- **Format:** YYYY-MM-DD
- **Type:** Date field

---

## Error Handling

### Common Errors:

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**Solution:** Include valid token in Authorization header

**400 Bad Request:**
```json
{
  "first_name": ["This field may not be blank."]
}
```
**Solution:** Provide required fields

**400 Wrong Password:**
```json
{
  "old_password": "Wrong password."
}
```
**Solution:** Verify current password is correct

---

## Summary

✅ **Backend is ready** - No changes needed  
✅ **Users can update** - Own profile anytime  
✅ **Security enforced** - Users can't change email or role  
✅ **File uploads** - Profile pictures supported  
✅ **Password management** - Users can change passwords  
✅ **Extended profiles** - Bio and preferences available  

**Users have full control over their own profiles while admins maintain security!** 🎉

