# Security Enhancements Implemented

This document outlines all security improvements made to the Spa Central admin dashboard.

## ✅ Completed Security Fixes

### 1. Backend Authorization ✓

**Problem:** All API endpoints were accessible with just authentication, no role-based access control.

**Fix:**
- Created `apps/users/permissions.py` with custom permission classes:
  - `IsAdminUser` - Only admin users can access
  - `IsSpaOwner` - Only spa owners
  - `IsSpaManager` - Only spa managers  
  - `IsOwnerOrAdmin` - Owner of resource or admin
  - `IsAdminOrReadOnly` - Admin can edit, others read-only

- Applied `IsAdminUser` permission to all viewsets:
  - Users (UserViewSet)
  - Spa Owners (PrimaryOwner, SecondaryOwner, ThirdOwner, FourthOwner)
  - Spas (SpaViewSet)
  - Spa Managers (SpaManagerViewSet)
  - Machines (MachineViewSet, AccountHolderViewSet)
  - Documents (All document viewsets)
  - Locations (StateViewSet, CityViewSet, AreaViewSet)

**Impact:** 🔒 **CRITICAL** - Now only admin users can access the admin dashboard APIs.

---

### 2. File Upload Security ✓

**Problem:** 
- Frontend allowed 30MB but backend only accepted 10MB
- No file type validation
- No malware protection

**Fix:**
- Created `apps/documents/validators.py` with:
  - File extension whitelist (PDF, DOC, images, etc.)
  - MIME type validation
  - File size validation (30MB max)
  
- Updated Django settings:
  ```python
  FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024  # 30MB
  DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024  # 30MB
  ```

- Applied validators to all file fields in models:
  - Document.file
  - OwnerDocument.file
  - SpaManagerDocument.file

- Fixed frontend validation to match (30MB)

**Allowed File Types:**
- Documents: .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx
- Images: .jpg, .jpeg, .png, .gif, .webp, .svg
- Text: .txt, .csv

**Impact:** 🛡️ **HIGH** - Prevents upload of malicious files (.exe, .sh, .bat, etc.)

---

### 3. Rate Limiting ✓

**Problem:** No rate limiting on login endpoint - vulnerable to brute force attacks.

**Fix:**
- Added throttle classes to `apps/users/throttles.py`:
  - `LoginRateThrottle` - 5 attempts per hour
  - `LoginDailyThrottle` - 20 attempts per day

- Applied to `EmailPasswordLoginView`:
  ```python
  throttle_classes = [BurstRateThrottle, LoginRateThrottle, LoginDailyThrottle]
  ```

**Rate Limits:**
- Login: 2/minute (burst), 5/hour, 20/day
- OTP Request: 3/hour, 10/day
- Password Reset: 3/hour, 5/day
- OTP Verify: 10/hour

**Impact:** 🛡️ **HIGH** - Prevents brute force login attacks.

---

### 4. CORS Configuration ✓

**Problem:** In DEBUG mode, allowed ALL origins (security risk).

**Fix:**
```python
# Only specific origins allowed
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://companydos.api.d0s369.co.in'
]

# In production, CORS_ALLOW_ALL_ORIGINS = False
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False
```

**Impact:** 🛡️ **MEDIUM** - Prevents unauthorized domains from accessing API.

---

### 5. Environment Variables ✓

**Problem:** No .env files for frontend - API URLs hardcoded.

**Fix:**
- Created `ENV_SETUP.md` with instructions
- Configured Vite to use environment variables
- Users need to create:
  - `.env.development` for local development
  - `.env.production` for production builds

**Impact:** 🔧 **MEDIUM** - Better configuration management.

---

### 6. Console Logs in Production ✓

**Problem:** Sensitive data potentially logged to browser console in production.

**Fix:**
- Updated `vite.config.js`:
  ```javascript
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
  }
  ```

**Impact:** 🔒 **MEDIUM** - Prevents data leakage through console logs.

---

## 🔄 Recommended Future Enhancements

### 1. Token Expiration (Not Fully Implemented)

**Current State:** Tokens never expire unless manually deleted.

**Recommendation:**
1. Use Django REST Framework's Token with expiration
2. Or implement JWT tokens with refresh tokens
3. Set token lifetime to 24 hours
4. Add auto-logout on token expiration

**How to Implement:**
```bash
# Run this cron job daily to clean up old tokens
python manage.py delete_expired_tokens --days 7
```

---

### 2. WebSocket Token Security

**Current Issue:** Token passed in WebSocket URL query string.

**Recommendation:**
- Use WebSocket subprotocols for authentication
- Or send token in first message after connection
- Avoid logging WebSocket URLs

---

### 3. Content Security Policy (CSP)

**Recommendation:**
Add CSP headers to `settings.py`:
```python
if not DEBUG:
    SECURE_CONTENT_SECURITY_POLICY = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline';"
    )
```

---

### 4. Two-Factor Authentication (2FA)

**Recommendation:**
- Add 2FA for admin users
- Use TOTP (Time-based One-Time Password)
- Make it mandatory for admin accounts

---

### 5. Audit Logging

**Recommendation:**
- Log all admin actions (create, update, delete)
- Track login attempts (successful and failed)
- Store IP addresses and timestamps
- Create audit trail for compliance

---

### 6. Session Security

**Recommendation:**
- Implement session timeout (15-30 minutes of inactivity)
- Add "remember me" option with longer expiration
- Invalidate all sessions on password change

---

### 7. File Malware Scanning

**Recommendation:**
- Integrate ClamAV or similar for production
- Scan all uploaded files before storage
- Quarantine suspicious files

---

## 📋 Security Checklist

- [x] Backend admin-only authorization
- [x] File upload validation and size limits
- [x] Rate limiting on authentication endpoints
- [x] CORS properly configured
- [x] Console logs removed in production
- [x] Environment variables documented
- [ ] Token expiration implemented
- [ ] WebSocket security improved
- [ ] CSP headers added
- [ ] 2FA for admin users
- [ ] Audit logging
- [ ] File malware scanning

---

## 🚀 Deployment Notes

### Before Deploying to Production:

1. **Set Environment Variables:**
   ```bash
   DEBUG=False
   SECRET_KEY=<generate-strong-secret-key>
   ALLOWED_HOSTS=your-production-domain.com
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

2. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Build Frontend:**
   ```bash
   cd frontend/Dashboard/admindashbboard
   npm run build
   ```

4. **Test Security:**
   - Try accessing API without admin token
   - Test file upload with different file types
   - Try brute force login (should be rate limited)
   - Verify CORS settings

5. **Set up Token Cleanup Cron Job:**
   ```bash
   # Add to crontab
   0 2 * * * cd /path/to/project && python manage.py delete_expired_tokens --days 7
   ```

---

## 🔍 Testing Security

### Test Admin Authorization:
```bash
# Should fail - no token
curl http://localhost:8000/api/users/

# Should fail - non-admin token
curl -H "Authorization: Token <spa-manager-token>" http://localhost:8000/api/users/

# Should succeed - admin token
curl -H "Authorization: Token <admin-token>" http://localhost:8000/api/users/
```

### Test Rate Limiting:
```bash
# Try logging in 6 times in quick succession
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}'
  sleep 1
done
# 6th attempt should return 429 Too Many Requests
```

### Test File Upload:
```bash
# Should fail - .exe file
curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Token <admin-token>" \
  -F "file=@malware.exe"

# Should succeed - .pdf file under 30MB
curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Token <admin-token>" \
  -F "file=@document.pdf"
```

---

## 📞 Support

For security issues or questions, contact the development team.

**Last Updated:** October 15, 2025

