"""
Utility functions for user management
"""

import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP, User


def generate_otp_code(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))


def create_otp(user, purpose='login', validity_minutes=10):
    """
    Create and return a new OTP for the user
    
    Args:
        user: User instance
        purpose: Purpose of OTP (login, registration, password_reset)
        validity_minutes: How long the OTP should be valid (default: 10 minutes)
    
    Returns:
        OTP instance
    """
    # Invalidate all previous unused OTPs for this user and purpose
    OTP.objects.filter(
        user=user,
        purpose=purpose,
        is_used=False
    ).update(is_used=True)
    
    # Generate new OTP
    code = generate_otp_code()
    expires_at = timezone.now() + timedelta(minutes=validity_minutes)
    
    otp = OTP.objects.create(
        user=user,
        code=code,
        purpose=purpose,
        expires_at=expires_at
    )
    
    return otp


def send_otp_email(user, otp, purpose='login'):
    """
    Send OTP via email
    
    Args:
        user: User instance
        otp: OTP instance
        purpose: Purpose of the OTP
    
    Returns:
        Boolean indicating success
    """
    purpose_text = {
        'login': 'Login',
        'registration': 'Registration',
        'password_reset': 'Password Reset'
    }.get(purpose, 'Authentication')
    
    subject = f'Your {purpose_text} OTP - Disha Online Solution'
    
    message = f"""
Hello {user.first_name or user.email},

Your OTP code for {purpose_text} is:

{otp.code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Disha Online Solution Team
    """
    
    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ background: #f9f9f9; padding: 20px; }}
        .otp-code {{ 
            font-size: 32px; 
            font-weight: bold; 
            color: #4CAF50; 
            text-align: center; 
            padding: 20px;
            background: white;
            border: 2px dashed #4CAF50;
            border-radius: 5px;
            margin: 20px 0;
            letter-spacing: 5px;
        }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        .warning {{ color: #f44336; font-size: 14px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Disha Online Solution</h1>
            <p>{purpose_text} Verification</p>
        </div>
        <div class="content">
            <p>Hello <strong>{user.first_name or user.email}</strong>,</p>
            <p>Your OTP code for {purpose_text} is:</p>
            <div class="otp-code">{otp.code}</div>
            <p><strong>This code will expire in 10 minutes.</strong></p>
            <p class="warning">⚠️ If you didn't request this code, please ignore this email and ensure your account is secure.</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 Disha Online Solution. All rights reserved.</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@dishaonlinesoution.com',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False


def verify_otp(email, code, purpose='login'):
    """
    Verify OTP code for a user
    
    Args:
        email: User's email
        code: OTP code to verify
        purpose: Purpose of the OTP
    
    Returns:
        Tuple (success: bool, message: str, user: User or None)
    """
    try:
        user = User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return False, "User not found", None
    
    try:
        otp = OTP.objects.get(
            user=user,
            code=code,
            purpose=purpose,
            is_used=False
        )
    except OTP.DoesNotExist:
        return False, "Invalid OTP code", None
    
    if not otp.is_valid():
        return False, "OTP has expired", None
    
    # Mark OTP as used
    otp.mark_as_used()
    
    return True, "OTP verified successfully", user


def get_or_create_user_by_email(email, **extra_fields):
    """
    Get existing user or create new one by email
    
    Args:
        email: User's email
        **extra_fields: Additional fields for user creation
    
    Returns:
        Tuple (user: User, created: bool)
    """
    email = email.lower()
    
    try:
        user = User.objects.get(email=email)
        return user, False
    except User.DoesNotExist:
        # Create new user
        user = User.objects.create_user(
            email=email,
            **extra_fields
        )
        return user, True

