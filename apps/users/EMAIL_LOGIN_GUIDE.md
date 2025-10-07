# Email-Based Login Guide

The User model has been configured to use **email** as the primary authentication field instead of username.

## Key Changes

1. **Username Field**: Email is now the `USERNAME_FIELD`
2. **Email**: Required and must be unique
3. **Username**: Optional (auto-generated from email if not provided)

## User Registration

### API Endpoint
```http
POST /api/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "employee",
    "phone": "+1234567890"
}
```

### Response
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "employee",
    "phone": "+1234567890",
    "is_verified": false,
    "created_at": "2024-01-01T10:00:00Z"
}
```

## User Login

### Obtain Authentication Token
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "securepassword123"
}
```

**Note**: The field is still called "username" in the API request for compatibility with DRF's TokenAuthentication, but you should provide the **email address** as the value.

### Response
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## Using the Token

Include the token in all authenticated requests:

```http
GET /api/users/me/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Django Admin

When logging into the Django admin panel at `/admin/`, use:
- **Email address** as username
- **Password**

Example:
- Email: `admin@example.com`
- Password: `your_password`

## Creating Superuser

When creating a superuser via command line:

```bash
python manage.py createsuperuser
```

You'll be prompted for:
1. **Email address** (required)
2. **First name** (required)
3. **Last name** (required)
4. **Password** (required)

## User Types

The system supports four user types:
- `manager`: Manager
- `owner`: Owner
- `employee`: Employee (default)
- `admin`: Admin

## Example: Python Code

### Create User Programmatically
```python
from apps.users.models import User

# Create a regular user
user = User.objects.create_user(
    email='user@example.com',
    password='securepassword',
    first_name='John',
    last_name='Doe',
    user_type='employee'
)

# Create a superuser
superuser = User.objects.create_superuser(
    email='admin@example.com',
    password='adminpassword',
    first_name='Admin',
    last_name='User'
)
```

### Authenticate User
```python
from django.contrib.auth import authenticate

# Authenticate by email
user = authenticate(username='user@example.com', password='securepassword')
if user is not None:
    # User is authenticated
    print(f"Logged in as: {user.email}")
else:
    # Authentication failed
    print("Invalid credentials")
```

## Migration Notes

If you're migrating from username-based to email-based authentication:

1. **Make sure all existing users have email addresses**
2. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Update any existing code** that references `username` to use `email`

## Frontend Integration

### Login Form Example
```javascript
// Login with email
async function login(email, password) {
    const response = await fetch('http://localhost:8000/api/auth/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: email,  // Note: field name is still 'username'
            password: password
        })
    });
    
    const data = await response.json();
    if (response.ok) {
        localStorage.setItem('token', data.token);
        return data.token;
    } else {
        throw new Error('Login failed');
    }
}

// Register new user
async function register(userData) {
    const response = await fetch('http://localhost:8000/api/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: userData.email,
            password: userData.password,
            password2: userData.password,
            first_name: userData.firstName,
            last_name: userData.lastName,
            user_type: 'employee'
        })
    });
    
    return await response.json();
}

// Use token for authenticated requests
async function getProfile(token) {
    const response = await fetch('http://localhost:8000/api/users/me/', {
        headers: {
            'Authorization': `Token ${token}`
        }
    });
    
    return await response.json();
}
```

## Testing

### Test Login
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password123"}'

# Use token
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Troubleshooting

### "This field is required" error for username
- Make sure you're using the updated User model
- Run migrations: `python manage.py migrate`

### Cannot login to admin
- Use your **email address** instead of username
- Clear browser cache if still having issues

### Email already exists error
- Each email must be unique in the system
- Check if user already exists before registration

## Security Best Practices

1. **Always use HTTPS** in production
2. **Validate email format** on frontend and backend
3. **Use strong passwords** (enforced by Django's password validators)
4. **Implement rate limiting** for login attempts
5. **Enable email verification** for new registrations
6. **Store tokens securely** on the client side
7. **Implement token refresh** for long-lived sessions

## Additional Resources

- [Django Authentication Documentation](https://docs.djangoproject.com/en/5.0/topics/auth/)
- [DRF Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
- [Custom User Models](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model)

