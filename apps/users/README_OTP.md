# Users App - OTP Authentication

## Quick Start

The users app now supports **OTP (One-Time Password) authentication** via email.

## Features Implemented

✅ **Email-based Login** - Users login using their email address  
✅ **OTP Authentication** - 6-digit code sent to email  
✅ **Passwordless Login** - No password required (OTP only)  
✅ **Auto-Expiry** - OTPs expire after 10 minutes  
✅ **Single Use** - Each OTP can only be used once  
✅ **Multiple Purposes** - Login, Registration, Password Reset  

## Files Created/Modified

### New Files
- `apps/users/models.py` - Added `OTP` model
- `apps/users/utils.py` - OTP generation and email sending utilities
- `apps/users/OTP_LOGIN_GUIDE.md` - Complete OTP implementation guide

### Modified Files
- `apps/users/serializers.py` - Added `RequestOTPSerializer`, `VerifyOTPSerializer`, `OTPSerializer`
- `apps/users/views.py` - Added `RequestOTPView`, `VerifyOTPView`, `OTPViewSet`
- `apps/users/urls.py` - Added OTP endpoints
- `apps/users/admin.py` - Added OTP admin interface
- `spa_central/settings.py` - Updated email configuration

## API Endpoints

### 1. Request OTP
```http
POST /api/auth/request-otp/

{
    "email": "user@example.com",
    "purpose": "login"  // or "registration" or "password_reset"
}
```

### 2. Verify OTP & Login
```http
POST /api/auth/verify-otp/

{
    "email": "user@example.com",
    "code": "123456",
    "purpose": "login"
}
```

### 3. View OTP History (Authenticated)
```http
GET /api/otps/
Authorization: Token YOUR_TOKEN
```

## User Types

- `manager` - Manager role
- `spa_manager` - Spa Manager role
- `employee` - Employee role (default)
- `admin` - Admin role

## Quick Test

### 1. Request OTP
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "purpose": "login"}'
```

### 2. Check Console
Look for OTP code in terminal (development mode)

### 3. Verify OTP
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "code": "123456", "purpose": "login"}'
```

### 4. Use Token
```bash
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Database Migrations

Run migrations to create OTP table:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Email Configuration

### Development
Emails print to console:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production
Use real SMTP server:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Security Features

1. **OTP Expiration** - 10 minutes validity
2. **Single Use** - Cannot reuse OTP codes
3. **Auto-Invalidation** - Old OTPs invalidated on new request
4. **Secure Codes** - Random 6-digit codes
5. **Email Verification** - OTP sent only to registered email

## Admin Panel

Access OTP management at:
- **URL**: `/admin/users/otp/`
- **Features**:
  - View all OTP requests
  - See OTP validity status
  - Track usage and expiry
  - Monitor user authentication

## Complete Flow

### Login Flow
1. User enters email
2. System sends OTP to email
3. User enters OTP code
4. System verifies code
5. User receives auth token
6. User makes authenticated requests

### Registration Flow
1. New user enters email
2. System creates temp user and sends OTP
3. User enters OTP + details (name, phone)
4. System verifies and completes registration
5. User receives auth token

## Documentation

📚 **Complete Guide**: `apps/users/OTP_LOGIN_GUIDE.md`  
📧 **Email Setup**: See `.env.example` for email configuration  
🔐 **Security**: OTP codes are single-use and expire in 10 minutes  

## Support

For issues:
1. Check `OTP_LOGIN_GUIDE.md` for detailed documentation
2. Verify email configuration in settings
3. Check Django admin for OTP history
4. Review application logs for errors

## Next Steps

Consider implementing:
- [ ] Rate limiting on OTP requests
- [ ] SMS-based OTP as alternative
- [ ] Remember device functionality
- [ ] OTP resend with cooldown
- [ ] Multi-factor authentication
- [ ] Login history tracking

