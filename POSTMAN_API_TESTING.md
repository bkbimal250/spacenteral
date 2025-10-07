# 🧪 Postman API Testing Guide - Dual Login System

## Base URL
```
http://localhost:8000
```

---

## 🎯 Two Login Methods Available

1. **Direct Login** - Email + Password (Instant)
2. **OTP Login** - Email + OTP Code (2-step)

---

## Method 1: 🔑 Direct Email + Password Login

### **Quick Login (Single Request)**

**Endpoint:** `POST /api/auth/login/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "user@example.com",
    "password": "yourpassword123"
}
```

**Expected Response (200 OK):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "employee",
        "is_verified": true
    },
    "message": "Login successful"
}
```

**Error Response (400):**
```json
{
    "detail": "Invalid email or password."
}
```

**✅ Advantages:** Instant, no email waiting, familiar

---

## Method 2: 📧 OTP Email Login

### 📋 Test Flow: Complete OTP Login

### **Step 1: Request OTP (Send OTP to Email)**

**Endpoint:** `POST /api/auth/request-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "your-email@gmail.com",
    "purpose": "login"
}
```

**Expected Response (200 OK):**
```json
{
    "email": "your-email@gmail.com",
    "message": "OTP sent to your-email@gmail.com",
    "expires_in_minutes": 10
}
```

**What happens:**
- OTP is generated
- Email is sent to your inbox
- Check your email for 6-digit code
- Code expires in 10 minutes

---

### **Step 2: Verify OTP & Login**

**Endpoint:** `POST /api/auth/verify-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "your-email@gmail.com",
    "code": "123456",
    "purpose": "login"
}
```
*Replace `123456` with the actual OTP from your email*

**Expected Response (200 OK):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
        "id": 1,
        "email": "your-email@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "employee",
        "phone": "+1234567890",
        "profile_picture": null,
        "date_of_birth": null,
        "address": null,
        "is_verified": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z",
        "profile": {
            "bio": null,
            "preferences": {},
            "notification_settings": {}
        }
    },
    "message": "Login successful"
}
```

**Important:** Save the `token` value for authenticated requests!

---

## 🆕 New User Registration with OTP

### **Step 1: Request OTP for Registration**

**Endpoint:** `POST /api/auth/request-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "newuser@gmail.com",
    "purpose": "registration"
}
```

**Expected Response (200 OK):**
```json
{
    "email": "newuser@gmail.com",
    "message": "OTP sent to newuser@gmail.com",
    "expires_in_minutes": 10
}
```

---

### **Step 2: Verify OTP & Complete Registration**

**Endpoint:** `POST /api/auth/verify-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "newuser@gmail.com",
    "code": "123456",
    "purpose": "registration",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
}
```

**Expected Response (200 OK):**
```json
{
    "token": "auth_token_here",
    "user": {
        "id": 2,
        "email": "newuser@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "user_type": "employee",
        "phone": "+1234567890",
        "is_verified": true,
        ...
    },
    "message": "Login successful"
}
```

---

## 🔐 Authenticated Requests (Use Token)

### **Get Current User Profile**

**Endpoint:** `GET /api/users/me/`

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```
*Replace with your actual token*

**No Request Body**

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "email": "your-email@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "employee",
    "phone": "+1234567890",
    "profile_picture": null,
    "date_of_birth": null,
    "address": null,
    "is_verified": true,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
    "profile": {
        "bio": null,
        "preferences": {},
        "notification_settings": {}
    }
}
```

---

### **Update User Profile**

**Endpoint:** `PATCH /api/users/me/`

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "first_name": "Updated Name",
    "last_name": "Updated Last",
    "phone": "+9876543210",
    "address": "123 Main Street"
}
```

**Expected Response (200 OK):**
```json
{
    "id": 1,
    "email": "your-email@gmail.com",
    "first_name": "Updated Name",
    "last_name": "Updated Last",
    "phone": "+9876543210",
    "address": "123 Main Street",
    ...
}
```

---

### **View OTP History**

**Endpoint:** `GET /api/otps/`

**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**No Request Body**

**Expected Response (200 OK):**
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "user_email": "your-email@gmail.com",
            "code": "***456",
            "purpose": "login",
            "is_used": true,
            "is_valid": false,
            "expires_at": "2024-01-01T10:10:00Z",
            "created_at": "2024-01-01T10:00:00Z",
            "used_at": "2024-01-01T10:01:00Z"
        }
    ]
}
```

---

## 🔄 Password Reset with OTP

### **Step 1: Request OTP for Password Reset**

**Endpoint:** `POST /api/auth/request-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "your-email@gmail.com",
    "purpose": "password_reset"
}
```

**Expected Response (200 OK):**
```json
{
    "email": "your-email@gmail.com",
    "message": "OTP sent to your-email@gmail.com",
    "expires_in_minutes": 10
}
```

---

### **Step 2: Verify OTP for Password Reset**

**Endpoint:** `POST /api/auth/verify-otp/`

**Headers:**
```
Content-Type: application/json
```

**Request Body (Raw JSON):**
```json
{
    "email": "your-email@gmail.com",
    "code": "123456",
    "purpose": "password_reset"
}
```

**Expected Response (200 OK):**
```json
{
    "token": "temp_reset_token",
    "user": {...},
    "message": "Login successful"
}
```

---

## 🚫 Error Responses

### Invalid OTP Code
**Status:** 400 Bad Request
```json
{
    "code": ["Invalid OTP code"]
}
```

### Expired OTP
**Status:** 400 Bad Request
```json
{
    "code": ["OTP has expired"]
}
```

### User Not Found (Login)
**Status:** 400 Bad Request
```json
{
    "email": ["No user found with this email address."]
}
```

### Missing Required Fields
**Status:** 400 Bad Request
```json
{
    "email": ["This field is required."],
    "code": ["This field is required."]
}
```

### Unauthorized (No Token)
**Status:** 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token
**Status:** 401 Unauthorized
```json
{
    "detail": "Invalid token."
}
```

---

## 📝 Postman Collection Setup

### Create Collection: "Spa Central - OTP Auth"

#### **1. Environment Variables**

Create environment with:
```
base_url: http://localhost:8000
token: (leave empty, will be set after login)
```

#### **2. Collection Variables**

In your collection, add:
- `{{base_url}}` - Base API URL
- `{{token}}` - Authentication token

#### **3. Test Scripts**

After "Verify OTP" request, add this test script:
```javascript
// Save token to environment
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.token);
    console.log("Token saved:", jsonData.token);
}
```

---

## 🔍 Complete Test Scenario

### **Scenario 1: First-Time User Registration**

1. **Request OTP** → `POST /api/auth/request-otp/`
   - Purpose: `registration`
   - Check email for OTP

2. **Verify & Register** → `POST /api/auth/verify-otp/`
   - Enter OTP + user details
   - Save token

3. **Get Profile** → `GET /api/users/me/`
   - Use saved token
   - Verify user details

---

### **Scenario 2: Existing User Login**

1. **Request OTP** → `POST /api/auth/request-otp/`
   - Purpose: `login`
   - Check email for OTP

2. **Verify & Login** → `POST /api/auth/verify-otp/`
   - Enter OTP
   - Save token

3. **Access Protected Route** → `GET /api/users/me/`
   - Use token

4. **Update Profile** → `PATCH /api/users/me/`
   - Use token
   - Update user info

5. **View OTP History** → `GET /api/otps/`
   - Use token
   - See all OTP requests

---

## ⚡ Quick Copy-Paste Examples

### Example 1: Login Flow
```bash
# 1. Request OTP
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com","purpose":"login"}'

# 2. Verify OTP (check email for code)
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com","code":"123456","purpose":"login"}'

# 3. Get profile (use token from step 2)
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Example 2: Registration Flow
```bash
# 1. Request OTP for registration
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@gmail.com","purpose":"registration"}'

# 2. Verify OTP and register
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"newuser@gmail.com",
    "code":"123456",
    "purpose":"registration",
    "first_name":"John",
    "last_name":"Doe",
    "phone":"+1234567890"
  }'
```

---

## 🎯 Testing Checklist

- [ ] Request OTP for new user (registration)
- [ ] Receive email with OTP code
- [ ] Verify OTP and complete registration
- [ ] Receive authentication token
- [ ] Use token to get user profile
- [ ] Update user profile with token
- [ ] Request OTP for existing user (login)
- [ ] Verify OTP and login
- [ ] View OTP history
- [ ] Test expired OTP (wait 11 minutes)
- [ ] Test invalid OTP code
- [ ] Test duplicate OTP usage

---

## 💡 Pro Tips

1. **Save Token**: Use Postman environment variables to save tokens
2. **Check Email**: Always check spam folder if OTP not received
3. **Time Limit**: OTP expires in 10 minutes
4. **One-Time Use**: Each OTP can only be used once
5. **Real Email**: Use a real email address you can access
6. **Test Account**: Create a test Gmail account for testing

---

## 🐛 Common Issues

### Issue: OTP not received
**Solution:** 
- Check spam/junk folder
- Verify email in request body
- Check server logs

### Issue: "Invalid OTP"
**Solution:**
- Check if OTP expired (10 min)
- Verify correct code from email
- Request new OTP

### Issue: "Unauthorized" error
**Solution:**
- Add `Authorization` header
- Use format: `Token YOUR_TOKEN_HERE`
- Verify token is correct

---

## 📱 Postman Import

Create a new collection with these requests or import from JSON:

```json
{
    "info": {
        "name": "Spa Central - OTP Auth",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Request OTP",
            "request": {
                "method": "POST",
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {
                    "mode": "raw",
                    "raw": "{\"email\":\"test@gmail.com\",\"purpose\":\"login\"}"
                },
                "url": {
                    "raw": "{{base_url}}/api/auth/request-otp/",
                    "host": ["{{base_url}}"],
                    "path": ["api", "auth", "request-otp", ""]
                }
            }
        },
        {
            "name": "Verify OTP",
            "request": {
                "method": "POST",
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "body": {
                    "mode": "raw",
                    "raw": "{\"email\":\"test@gmail.com\",\"code\":\"123456\",\"purpose\":\"login\"}"
                },
                "url": {
                    "raw": "{{base_url}}/api/auth/verify-otp/",
                    "host": ["{{base_url}}"],
                    "path": ["api", "auth", "verify-otp", ""]
                }
            }
        },
        {
            "name": "Get Current User",
            "request": {
                "method": "GET",
                "header": [{"key": "Authorization", "value": "Token {{token}}"}],
                "url": {
                    "raw": "{{base_url}}/api/users/me/",
                    "host": ["{{base_url}}"],
                    "path": ["api", "users", "me", ""]
                }
            }
        }
    ]
}
```

---

**Happy Testing! 🚀**

For more details, check:
- `EMAIL_SETUP_COMPLETE.md`
- `FINAL_SETUP_GUIDE.md`
- `apps/users/OTP_LOGIN_GUIDE.md`

