# 🔐 Dual Login System - Complete Guide

## Two Ways to Login

Your system now supports **TWO** login methods:

1. **🔑 Direct Email + Password Login** (Traditional, instant)
2. **📧 OTP Email Login** (Passwordless, more secure)

---

## Method 1: Email + Password Login (Direct)

### 📍 Endpoint
```
POST /api/auth/login/
```

### 📝 Request
**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "email": "user@example.com",
    "password": "yourpassword123"
}
```

### ✅ Success Response (200 OK)
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "employee",
        "phone": "+1234567890",
        "is_verified": true,
        "created_at": "2024-01-01T10:00:00Z"
    },
    "message": "Login successful"
}
```

### ❌ Error Response (400 Bad Request)
```json
{
    "detail": "Invalid email or password."
}
```

### ⚡ Advantages
- ✅ **Instant login** - No waiting for email
- ✅ **Works offline** - No internet needed after initial setup
- ✅ **Familiar** - Traditional login method
- ✅ **Fast** - One-step process

### 🔧 Postman Setup

**Method:** `POST`  
**URL:** `http://localhost:8000/api/auth/login/`  
**Headers:**
```
Content-Type: application/json
```
**Body (raw JSON):**
```json
{
    "email": "test@gmail.com",
    "password": "Test@123"
}
```

---

## Method 2: OTP Email Login (Passwordless)

### Step 1: Request OTP

**Endpoint:** `POST /api/auth/request-otp/`

**Request:**
```json
{
    "email": "user@example.com",
    "purpose": "login"
}
```

**Response:**
```json
{
    "email": "user@example.com",
    "message": "OTP sent to user@example.com",
    "expires_in_minutes": 10
}
```

### Step 2: Verify OTP & Login

**Endpoint:** `POST /api/auth/verify-otp/`

**Request:**
```json
{
    "email": "user@example.com",
    "code": "123456",
    "purpose": "login"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {...},
    "message": "Login successful"
}
```

### ⚡ Advantages
- ✅ **No password needed** - Passwordless authentication
- ✅ **More secure** - Temporary, single-use codes
- ✅ **Email verification** - Confirms email ownership
- ✅ **Password recovery** - No need to remember password

---

## 📊 Comparison Table

| Feature | Email + Password | OTP Email |
|---------|-----------------|-----------|
| **Speed** | ⚡ Instant | 🐢 2-step (wait for email) |
| **Security** | 🔒 Good | 🔐 Excellent |
| **User Experience** | 😊 Familiar | 🤔 Modern |
| **Password Required** | ✅ Yes | ❌ No |
| **Internet Required** | ❌ No | ✅ Yes |
| **Setup Complexity** | 🟢 Simple | 🟡 Moderate |
| **Best For** | Quick access | Forgot password, New devices |

---

## 🎯 Use Cases

### When to Use Email + Password
- ✅ Quick daily login
- ✅ User knows their password
- ✅ Fast access needed
- ✅ Offline environments

### When to Use OTP
- ✅ User forgot password
- ✅ First-time login
- ✅ Login from new device
- ✅ Enhanced security needed
- ✅ Passwordless preference

---

## 🔄 Complete User Flows

### Flow 1: New User Registration

**Option A: With Password**
```
1. POST /api/users/
   {
     "email": "new@example.com",
     "password": "Pass@123",
     "password2": "Pass@123",
     "first_name": "John",
     "last_name": "Doe"
   }

2. User created ✅

3. POST /api/auth/login/
   {
     "email": "new@example.com",
     "password": "Pass@123"
   }

4. Get token and login ✅
```

**Option B: With OTP**
```
1. POST /api/auth/request-otp/
   {
     "email": "new@example.com",
     "purpose": "registration"
   }

2. Check email for OTP

3. POST /api/auth/verify-otp/
   {
     "email": "new@example.com",
     "code": "123456",
     "purpose": "registration",
     "first_name": "John",
     "last_name": "Doe"
   }

4. User created and logged in ✅
```

### Flow 2: Existing User Login

**Option A: Direct Login**
```
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "Pass@123"
}

✅ Immediate login
```

**Option B: OTP Login**
```
1. POST /api/auth/request-otp/
   { "email": "user@example.com", "purpose": "login" }

2. Check email

3. POST /api/auth/verify-otp/
   { "email": "user@example.com", "code": "123456", "purpose": "login" }

✅ Login after verification
```

---

## 🧪 Postman Testing

### Test 1: Email + Password Login

**Request:**
```
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
    "email": "test@gmail.com",
    "password": "Test@123"
}
```

**Save Token:**
After successful login, save the token:
```javascript
// In Postman Tests tab
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.token);
}
```

### Test 2: OTP Login

**Step 1 - Request OTP:**
```
POST http://localhost:8000/api/auth/request-otp/
Content-Type: application/json

{
    "email": "test@gmail.com",
    "purpose": "login"
}
```

**Step 2 - Check Email, then Verify:**
```
POST http://localhost:8000/api/auth/verify-otp/
Content-Type: application/json

{
    "email": "test@gmail.com",
    "code": "123456",
    "purpose": "login"
}
```

---

## 🛡️ Security Considerations

### Email + Password Login
- ✅ Password stored securely (hashed)
- ✅ Django's built-in authentication
- ✅ Password validation rules
- ⚠️ Vulnerable to brute force (implement rate limiting)
- ⚠️ Password can be forgotten

### OTP Login
- ✅ No password storage concerns
- ✅ Temporary codes (10 minutes)
- ✅ Single-use OTPs
- ✅ Email ownership verification
- ⚠️ Requires email access
- ⚠️ Email can be intercepted (use HTTPS)

---

## 💡 Recommendations

### For Users
1. **Use Email+Password for daily login** (faster)
2. **Use OTP when:**
   - Forgot password
   - Login from new device
   - Enhanced security needed

### For Developers
1. **Implement rate limiting** on both endpoints
2. **Add 2FA** for sensitive operations
3. **Log failed login attempts**
4. **Monitor for suspicious activity**
5. **Use HTTPS in production**

### For System Admins
1. **Enable account lockout** after failed attempts
2. **Monitor login patterns**
3. **Set password policies**
4. **Regular security audits**

---

## 🔧 Configuration

### Enable/Disable Login Methods

To disable password login (OTP only):
```python
# In views.py - Remove EmailPasswordLoginView
# In urls.py - Remove login endpoint
```

To disable OTP login (password only):
```python
# In urls.py - Remove OTP endpoints
```

---

## 📝 API Summary

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| `POST` | `/api/auth/login/` | Email+Password login | ❌ No |
| `POST` | `/api/auth/request-otp/` | Request OTP | ❌ No |
| `POST` | `/api/auth/verify-otp/` | Verify OTP & login | ❌ No |
| `POST` | `/api/users/` | Register new user | ❌ No |
| `GET` | `/api/users/me/` | Get current user | ✅ Yes |
| `PATCH` | `/api/users/me/` | Update profile | ✅ Yes |
| `POST` | `/api/users/change_password/` | Change password | ✅ Yes |

---

## 🚀 Quick Start Commands

### Test Email + Password Login
```bash
# Register user
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@gmail.com",
    "password":"Test@123",
    "password2":"Test@123",
    "first_name":"Test",
    "last_name":"User"
  }'

# Login directly
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@gmail.com",
    "password":"Test@123"
  }'
```

### Test OTP Login
```bash
# Request OTP
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@gmail.com",
    "purpose":"login"
  }'

# Check email, then verify
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@gmail.com",
    "code":"123456",
    "purpose":"login"
  }'
```

---

## 📚 Documentation Files

- **DUAL_LOGIN_GUIDE.md** (this file) - Complete dual login guide
- **POSTMAN_API_TESTING.md** - Detailed Postman testing
- **EMAIL_SETUP_COMPLETE.md** - Email configuration
- **apps/users/OTP_LOGIN_GUIDE.md** - OTP-specific guide
- **FINAL_SETUP_GUIDE.md** - Complete setup instructions

---

## ✅ System Status

- ✅ Email + Password Login: **ACTIVE**
- ✅ OTP Email Login: **ACTIVE**
- ✅ Email Service: **Gmail SMTP Configured**
- ✅ Token Authentication: **ACTIVE**
- ✅ User Registration: **ACTIVE**

**Both login methods are ready to use!** 🎉

---

**Last Updated:** [Current Date]  
**Version:** 2.0 (Dual Login System)

