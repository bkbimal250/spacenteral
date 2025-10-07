# OTP (One-Time Password) Login Guide

## Overview

The system now supports **OTP-based authentication** via email. Users can login by receiving a one-time code sent to their email address instead of using a password.

## Features

✅ **Passwordless Login** - Login with just email and OTP  
✅ **Email-based OTP** - 6-digit code sent to user's email  
✅ **10-minute Validity** - OTPs expire after 10 minutes  
✅ **Multiple Purposes** - Login, Registration, Password Reset  
✅ **Secure** - OTPs can only be used once  
✅ **Auto-cleanup** - Old OTPs are invalidated when new ones are created  

## How It Works

### 1. Request OTP (Step 1)
User provides their email → System sends 6-digit code to email

### 2. Verify OTP (Step 2)
User enters the code → System verifies and logs them in

## API Endpoints

### 1. Request OTP

**Endpoint:** `POST /api/auth/request-otp/`

**Request Body:**
```json
{
    "email": "user@example.com",
    "purpose": "login"
}
```

**Purpose Options:**
- `login` - For existing user login
- `registration` - For new user registration
- `password_reset` - For password reset flow

**Response (Success):**
```json
{
    "email": "user@example.com",
    "message": "OTP sent to user@example.com",
    "expires_in_minutes": 10
}
```

**Response (Error):**
```json
{
    "email": ["No user found with this email address."]
}
```

### 2. Verify OTP

**Endpoint:** `POST /api/auth/verify-otp/`

**Request Body (Login):**
```json
{
    "email": "user@example.com",
    "code": "123456",
    "purpose": "login"
}
```

**Request Body (Registration - with user details):**
```json
{
    "email": "newuser@example.com",
    "code": "123456",
    "purpose": "registration",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
}
```

**Response (Success):**
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

**Response (Error):**
```json
{
    "code": ["Invalid OTP code"]
}
// or
{
    "code": ["OTP has expired"]
}
```

## Complete Login Flow

### Login for Existing User

```bash
# Step 1: Request OTP
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "purpose": "login"
  }'

# Response: Check email for 6-digit code

# Step 2: Verify OTP and Login
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "code": "123456",
    "purpose": "login"
  }'

# Response: Receive authentication token

# Step 3: Use token for authenticated requests
curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Registration for New User

```bash
# Step 1: Request OTP for registration
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "purpose": "registration"
  }'

# Step 2: Verify OTP and complete registration
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "code": "123456",
    "purpose": "registration",
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "+1234567890"
  }'

# Response: User is created and authenticated
```

## Frontend Integration

### React/JavaScript Example

```javascript
// OTP Login Component
class OTPLogin extends React.Component {
  state = {
    email: '',
    otp: '',
    step: 1, // 1: request OTP, 2: verify OTP
    loading: false,
    error: null
  };

  requestOTP = async () => {
    this.setState({ loading: true, error: null });
    
    try {
      const response = await fetch('http://localhost:8000/api/auth/request-otp/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.state.email,
          purpose: 'login'
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        this.setState({ step: 2, loading: false });
        alert('OTP sent to your email!');
      } else {
        this.setState({ error: data.email || 'Failed to send OTP', loading: false });
      }
    } catch (error) {
      this.setState({ error: 'Network error', loading: false });
    }
  };

  verifyOTP = async () => {
    this.setState({ loading: true, error: null });
    
    try {
      const response = await fetch('http://localhost:8000/api/auth/verify-otp/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: this.state.email,
          code: this.state.otp,
          purpose: 'login'
        })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        // Save token
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Redirect to dashboard
        window.location.href = '/dashboard';
      } else {
        this.setState({ 
          error: data.code || 'Invalid OTP', 
          loading: false 
        });
      }
    } catch (error) {
      this.setState({ error: 'Network error', loading: false });
    }
  };

  render() {
    const { email, otp, step, loading, error } = this.state;
    
    return (
      <div className="otp-login">
        <h2>Login with OTP</h2>
        
        {error && <div className="error">{error}</div>}
        
        {step === 1 ? (
          <div>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => this.setState({ email: e.target.value })}
            />
            <button onClick={this.requestOTP} disabled={loading}>
              {loading ? 'Sending...' : 'Send OTP'}
            </button>
          </div>
        ) : (
          <div>
            <p>OTP sent to {email}</p>
            <input
              type="text"
              placeholder="Enter 6-digit code"
              maxLength="6"
              value={otp}
              onChange={(e) => this.setState({ otp: e.target.value })}
            />
            <button onClick={this.verifyOTP} disabled={loading}>
              {loading ? 'Verifying...' : 'Verify & Login'}
            </button>
            <button onClick={() => this.setState({ step: 1 })}>
              Change Email
            </button>
          </div>
        )}
      </div>
    );
  }
}
```

## Email Configuration

### Development (Console Backend)

For development, emails are printed to console:

```python
# In .env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Check terminal/console to see the OTP codes.

### Production (SMTP Backend)

For production, configure real SMTP server:

```env
# In .env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Spa Central <noreply@spacentral.com>
```

#### Gmail Configuration

1. Enable 2-Factor Authentication
2. Generate App Password
3. Use App Password in `EMAIL_HOST_PASSWORD`

#### SendGrid Configuration

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

## Security Features

### 1. OTP Expiration
- OTPs expire after 10 minutes
- Expired OTPs cannot be used

### 2. Single Use
- Each OTP can only be used once
- Used OTPs are marked and cannot be reused

### 3. Auto-Invalidation
- When new OTP is requested, previous unused OTPs are invalidated
- Prevents multiple valid OTPs for same user

### 4. Rate Limiting (Recommended)
Implement rate limiting on OTP request endpoint:

```python
# Install: pip install django-ratelimit

from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')
def request_otp_view(request):
    # Your view logic
    pass
```

## Admin Interface

Admins can view OTP history in Django admin:

1. Go to `/admin/`
2. Navigate to **User OTPs**
3. View all OTP requests with:
   - User email
   - OTP code (masked if used)
   - Purpose (login/registration/password_reset)
   - Validity status
   - Created and expired times

## Testing

### Test OTP Flow

```python
# In Django shell
python manage.py shell

from apps.users.models import User, OTP
from apps.users.utils import create_otp, send_otp_email

# Create test user
user = User.objects.create_user(
    email='test@example.com',
    first_name='Test',
    last_name='User'
)

# Generate OTP
otp = create_otp(user, purpose='login')
print(f"OTP Code: {otp.code}")

# Send email (will print to console in development)
send_otp_email(user, otp, purpose='login')

# Verify OTP
from apps.users.utils import verify_otp
success, message, user = verify_otp('test@example.com', otp.code, 'login')
print(f"Verification: {success}, {message}")
```

## Troubleshooting

### OTP Not Received

1. **Check Console** (Development)
   - Look for email output in terminal

2. **Check Spam Folder** (Production)
   - OTP emails might be in spam

3. **Verify Email Settings**
   - Ensure SMTP settings are correct
   - Test email configuration

### Invalid OTP Error

- OTP might have expired (10 minutes)
- OTP might have been used already
- Wrong code entered
- Request new OTP

### User Not Found Error

- Email address doesn't exist in system
- Use 'registration' purpose for new users

## Best Practices

1. **Always use HTTPS** in production
2. **Implement rate limiting** on OTP requests
3. **Monitor OTP usage** for abuse
4. **Set short expiry** times (10 minutes recommended)
5. **Log OTP attempts** for security auditing
6. **Use transaction emails** for better deliverability
7. **Provide resend option** if OTP not received

## Migration from Password to OTP

Users can still use password-based login via `/api/auth/token/` endpoint. The OTP login is an additional authentication method, not a replacement.

To force OTP-only:
1. Disable password authentication endpoint
2. Update frontend to only show OTP login
3. Notify users about the change

## Support

For issues with OTP login:
- Check email configuration
- Review OTP admin panel
- Check application logs
- Test with console backend first

