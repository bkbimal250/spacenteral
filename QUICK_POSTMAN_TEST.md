# ⚡ Quick Postman Test - Both Login Methods

## 🎯 TWO Ways to Login

---

## Method 1: 🔑 Direct Login (Email + Password)

### **ONE REQUEST - INSTANT LOGIN**

**URL:** `http://localhost:8000/api/auth/login/`  
**Method:** `POST`  
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

**✅ Response:**
```json
{
    "token": "YOUR_AUTH_TOKEN_HERE",
    "user": { ... },
    "message": "Login successful"
}
```

**⚡ Use this for:** Quick daily login, when you know password

---

## Method 2: 📧 OTP Login (Email + Code)

### **TWO REQUESTS - SECURE LOGIN**

### Request 1: Get OTP Code

**URL:** `http://localhost:8000/api/auth/request-otp/`  
**Method:** `POST`  
**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "test@gmail.com",
    "purpose": "login"
}
```

**✅ Response:**
```json
{
    "message": "OTP sent to test@gmail.com",
    "expires_in_minutes": 10
}
```

**👉 Check your email for 6-digit code!**

---

### Request 2: Verify OTP & Login

**URL:** `http://localhost:8000/api/auth/verify-otp/`  
**Method:** `POST`  
**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "test@gmail.com",
    "code": "123456",
    "purpose": "login"
}
```
*Replace `123456` with code from email*

**✅ Response:**
```json
{
    "token": "YOUR_AUTH_TOKEN_HERE",
    "user": { ... },
    "message": "Login successful"
}
```

**⚡ Use this for:** Forgot password, new device, extra security

---

## 🆕 Register New User (With Password)

**URL:** `http://localhost:8000/api/users/`  
**Method:** `POST`  
**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "email": "newuser@gmail.com",
    "password": "StrongPass@123",
    "password2": "StrongPass@123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
}
```

**✅ Response:**
```json
{
    "id": 1,
    "email": "newuser@gmail.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

**After registration, use Method 1 to login!**

---

## 🔐 Use Token for Authenticated Requests

### Get Current User Profile

**URL:** `http://localhost:8000/api/users/me/`  
**Method:** `GET`  
**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
```

**No body needed**

**✅ Response:**
```json
{
    "id": 1,
    "email": "test@gmail.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

---

### Update Profile

**URL:** `http://localhost:8000/api/users/me/`  
**Method:** `PATCH`  
**Headers:**
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
    "first_name": "Updated Name",
    "phone": "+9876543210"
}
```

---

## 📊 Quick Comparison

| Feature | Direct Login | OTP Login |
|---------|-------------|-----------|
| **Requests** | 1 | 2 |
| **Speed** | ⚡ Instant | 🐢 Wait for email |
| **Password** | ✅ Required | ❌ Not needed |
| **Security** | 🔒 Good | 🔐 Better |
| **Best For** | Daily use | Forgot password |

---

## 🧪 Test Both Methods

### Step-by-Step Test

1. **Register** new user with password
2. **Login** using Method 1 (email + password)
3. Save the token
4. **Get profile** using token
5. **Logout** (delete token)
6. **Login** using Method 2 (OTP)
7. Verify both tokens work!

---

## 🎯 Postman Collection Structure

```
Spa Central API
│
├── Authentication
│   ├── Direct Login (Email+Password)
│   ├── Request OTP
│   ├── Verify OTP & Login
│   └── Register User
│
└── User Management
    ├── Get Current User
    ├── Update Profile
    └── View OTP History
```

---

## 💡 Pro Tips

1. **Save Token**: Add this to Postman Tests tab:
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.environment.set("token", jsonData.token);
   }
   ```

2. **Use Environment Variable**: 
   - Create variable: `{{token}}`
   - Use in headers: `Authorization: Token {{token}}`

3. **Test Real Email**: Use actual Gmail for OTP testing

4. **Check Spam**: OTP emails might go to spam folder

---

## 🚀 Ready-to-Use Requests

### Collection 1: Quick Login Test
```
1. POST /api/auth/login/
   Body: {"email":"test@gmail.com","password":"Test@123"}
   ✅ Get token

2. GET /api/users/me/
   Header: Authorization: Token {saved_token}
   ✅ View profile
```

### Collection 2: OTP Login Test
```
1. POST /api/auth/request-otp/
   Body: {"email":"test@gmail.com","purpose":"login"}
   ✅ Email sent

2. Check email for code

3. POST /api/auth/verify-otp/
   Body: {"email":"test@gmail.com","code":"123456","purpose":"login"}
   ✅ Get token

4. GET /api/users/me/
   Header: Authorization: Token {saved_token}
   ✅ View profile
```

---

## ✅ Checklist

- [ ] Postman installed
- [ ] Server running (`python manage.py runserver`)
- [ ] Test user created
- [ ] Tried Method 1 (Direct Login)
- [ ] Tried Method 2 (OTP Login)
- [ ] Token saved in environment
- [ ] Tested authenticated requests
- [ ] Both methods working! 🎉

---

**That's it! You now have TWO ways to login.** 🚀

Choose the one that fits your use case:
- **Quick access?** → Use Direct Login
- **Forgot password?** → Use OTP Login
- **Extra security?** → Use OTP Login
- **Daily login?** → Use Direct Login

Both methods return the same token format and work identically after login!

