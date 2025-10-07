# Quick Test - OTP Login

## Prerequisites

1. Make sure migrations are run:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Start the development server:
```bash
python manage.py runserver
```

3. Keep terminal visible to see OTP codes (console backend)

## Test Scenario 1: New User Registration with OTP

### Step 1: Request OTP for Registration
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "purpose": "registration"
  }'
```

**Expected Response:**
```json
{
    "email": "newuser@example.com",
    "message": "OTP sent to newuser@example.com",
    "expires_in_minutes": 10
}
```

**Check Console:** Look for OTP code in terminal

### Step 2: Verify OTP and Complete Registration
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "code": "REPLACE_WITH_OTP_FROM_CONSOLE",
    "purpose": "registration",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
  }'
```

**Expected Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "email": "newuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "employee",
        "phone": "+1234567890",
        "is_verified": true
    },
    "message": "Login successful"
}
```

### Step 3: Test Authenticated Request
```bash
# Replace TOKEN with the token from step 2
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Test Scenario 2: Existing User Login with OTP

### Step 1: Request OTP for Login
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "purpose": "login"
  }'
```

### Step 2: Verify OTP and Login
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "code": "REPLACE_WITH_OTP_FROM_CONSOLE",
    "purpose": "login"
  }'
```

## Test Scenario 3: Error Cases

### Test 1: Non-existent User
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nonexistent@example.com",
    "purpose": "login"
  }'
```

**Expected:** Error message - user not found

### Test 2: Invalid OTP
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "code": "000000",
    "purpose": "login"
  }'
```

**Expected:** Error message - invalid OTP

### Test 3: Expired OTP
Wait 11 minutes and try to verify an old OTP.

**Expected:** Error message - OTP has expired

## Using Python Shell

### Create User and Test OTP
```python
python manage.py shell

from apps.users.models import User, OTP
from apps.users.utils import create_otp, verify_otp, send_otp_email

# Create user
user = User.objects.create_user(
    email='test@example.com',
    first_name='Test',
    last_name='User',
    user_type='employee'
)

# Generate OTP
otp = create_otp(user, purpose='login')
print(f"OTP Code: {otp.code}")
print(f"Expires at: {otp.expires_at}")
print(f"Is valid: {otp.is_valid()}")

# Send email
send_otp_email(user, otp, purpose='login')

# Verify OTP
success, message, verified_user = verify_otp('test@example.com', otp.code, 'login')
print(f"Success: {success}")
print(f"Message: {message}")
print(f"User: {verified_user}")

# Try to verify again (should fail - already used)
success2, message2, verified_user2 = verify_otp('test@example.com', otp.code, 'login')
print(f"Second attempt - Success: {success2}, Message: {message2}")
```

## Check Django Admin

1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to **User OTPs**
4. View all OTP requests with status

## Troubleshooting

### Can't see OTP in console?
- Make sure `EMAIL_BACKEND` is set to `console` in settings
- Check terminal where `runserver` is running

### Getting "User not found" error?
- For login, user must exist
- Use 'registration' purpose for new users

### OTP expired immediately?
- Check system timezone settings
- Ensure `USE_TZ = True` in settings

### Can't import modules?
- Make sure all migrations are run
- Restart Django server after code changes

## Expected Console Output (Development)

When OTP is sent, you should see in console:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Your Login OTP - Spa Central
From: Spa Central <noreply@spacentral.com>
To: newuser@example.com

Hello newuser@example.com,

Your OTP code for Login is:

123456

This code will expire in 10 minutes.
...
```

Copy the 6-digit code and use it in the verify endpoint.

## Success Indicators

✅ Request OTP returns 200 status  
✅ OTP appears in console output  
✅ Verify OTP returns token  
✅ Token works for authenticated endpoints  
✅ Can see OTP in admin panel  
✅ Used OTP cannot be reused  
✅ Expired OTP shows error  

## Next Steps

After successful testing:
1. Configure production email backend (SMTP)
2. Implement rate limiting
3. Add frontend integration
4. Set up monitoring for OTP usage
5. Configure proper email templates

