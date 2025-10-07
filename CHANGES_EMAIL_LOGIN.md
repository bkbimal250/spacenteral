# Changes Made for Email-Based Login

## Summary
The user authentication system has been updated to use **email addresses** as the primary login credential instead of usernames.

## User Types Updated
Changed from:
- `customer` → `employee`
- `spa_owner` → `owner`
- Added: `manager`
- Kept: `admin`

New user types:
- **Manager**: Spa manager
- **Owner**: Spa owner (full control)
- **Employee**: Regular employee (default)
- **Admin**: System administrator

## Files Modified

### 1. `apps/users/models.py`
**Changes:**
- Set `USERNAME_FIELD = 'email'` (email is now the login identifier)
- Made `email` field required and unique
- Made `username` optional (auto-generated from email)
- Changed default user_type from `customer` to `employee`
- Updated `REQUIRED_FIELDS` to `['first_name', 'last_name']`
- Added auto-generation of username in `save()` method
- Updated `__str__` method to display email instead of username

### 2. `apps/users/serializers.py`
**Changes:**
- Removed `username` from registration serializer fields
- Made `email` the primary field in registration
- Added email validation (uniqueness check)
- Added email normalization (lowercase)
- Updated UserSerializer to show email instead of username
- Made email read-only after registration

### 3. `apps/users/admin.py`
**Changes:**
- Updated list_display to show email first
- Removed username from search_fields
- Reorganized fieldsets to prioritize email
- Updated add_fieldsets to require email instead of username
- Added readonly_fields for timestamps

### 4. `apps/spas/views.py`
**Changes:**
- Updated user type checks from `customer` to `employee`
- Updated user type checks from `spa_owner` to `owner` and `manager`

### 5. `apps/documents/views.py`
**Changes:**
- Updated user type checks from `spa_owner` to `owner` and `manager`
- Updated user type checks from `customer` to `employee`

### 6. `scripts/import_spas.py`
**Changes:**
- Changed from `username` to `email` when creating users
- Updated user type from `spa_owner` to `owner`
- Updated `get_or_create` to use email as lookup field

## New Files Created

### `apps/users/EMAIL_LOGIN_GUIDE.md`
Complete guide documenting:
- How to register users with email
- How to login with email
- API examples
- Frontend integration examples
- Django admin login instructions
- Troubleshooting tips
- Security best practices

## Migration Steps

If you already have a database with users, you'll need to:

1. **Delete existing database** (if in development):
   ```bash
   # Delete SQLite database
   rm db.sqlite3
   
   # Or drop PostgreSQL database
   dropdb spa_central_db
   createdb spa_central_db
   ```

2. **Delete existing migrations**:
   ```bash
   # Delete migration files (keep __init__.py)
   rm apps/users/migrations/0*.py
   rm apps/location/migrations/0*.py
   rm apps/spas/migrations/0*.py
   rm apps/documents/migrations/0*.py
   rm apps/chat/migrations/0*.py
   ```

3. **Create fresh migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create new superuser**:
   ```bash
   python manage.py createsuperuser
   # Enter email, first name, last name, and password
   ```

## How to Login Now

### API Login (Token Authentication)
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "password123"
  }'
```

**Note**: The field is still called `username` in the request for DRF compatibility, but you should provide the **email address**.

### Django Admin Login
Go to `http://localhost:8000/admin/` and login with:
- **Email**: `your-email@example.com`
- **Password**: `your-password`

### User Registration
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "employee"
  }'
```

## Testing the Changes

### 1. Create a test user via shell:
```python
python manage.py shell

from apps.users.models import User

# Create user
user = User.objects.create_user(
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User',
    user_type='employee'
)
print(f"Created user: {user.email}")
```

### 2. Test authentication:
```python
from django.contrib.auth import authenticate

user = authenticate(username='test@example.com', password='testpass123')
if user:
    print(f"Authentication successful: {user.email}")
else:
    print("Authentication failed")
```

### 3. Test API endpoints:
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test@example.com","password":"testpass123"}'

# Get profile
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Benefits of Email-Based Login

1. **User-Friendly**: Users remember emails better than usernames
2. **Unique Identifier**: Email is already unique and verified
3. **No Username Conflicts**: No need to check username availability
4. **Professional**: More common in modern applications
5. **Password Recovery**: Email is needed for password reset anyway

## Breaking Changes

⚠️ **Important**: These are breaking changes if you already have users in your database.

1. Existing usernames will not work for login
2. All users must have valid email addresses
3. User type values have changed
4. API responses will return `email` instead of `username`

## Rollback Instructions

If you need to revert to username-based authentication:

1. In `apps/users/models.py`:
   - Change `USERNAME_FIELD = 'email'` to `USERNAME_FIELD = 'username'`
   - Make `email` optional: `email = models.EmailField(blank=True)`
   - Make `username` required: `username = models.CharField(max_length=150, unique=True)`
   - Update `REQUIRED_FIELDS = []`

2. Revert serializers and admin changes
3. Run migrations
4. Update API documentation

## Support

For questions or issues:
- Check `EMAIL_LOGIN_GUIDE.md` in the users app
- Review API_DOCUMENTATION.md
- Contact development team

## Next Steps

Consider implementing:
- Email verification on registration
- Password reset via email
- Two-factor authentication (2FA)
- Social authentication (Google, Facebook, etc.)
- Rate limiting on login attempts
- Login history tracking

