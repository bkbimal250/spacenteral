"""
Custom throttle classes for rate limiting email sending
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class OTPRequestThrottle(AnonRateThrottle):
    """
    Limit OTP requests to prevent abuse
    - Anonymous users: 3 requests per hour
    """
    scope = 'otp_request'
    rate = '3/hour'


class OTPRequestDailyThrottle(AnonRateThrottle):
    """
    Daily limit for OTP requests
    - Anonymous users: 10 requests per day
    """
    scope = 'otp_request_daily'
    rate = '10/day'


class PasswordResetThrottle(AnonRateThrottle):
    """
    Limit password reset requests
    - Anonymous users: 3 requests per hour
    """
    scope = 'password_reset'
    rate = '3/hour'


class PasswordResetDailyThrottle(AnonRateThrottle):
    """
    Daily limit for password reset
    - Anonymous users: 5 requests per day
    """
    scope = 'password_reset_daily'
    rate = '5/day'


class OTPVerifyThrottle(AnonRateThrottle):
    """
    Limit OTP verification attempts to prevent brute force
    - Anonymous users: 10 attempts per hour
    """
    scope = 'otp_verify'
    rate = '10/hour'


class EmailSendingThrottle(AnonRateThrottle):
    """
    General email sending throttle for authenticated users
    - Authenticated users: 20 emails per hour
    """
    scope = 'email_sending'
    rate = '20/hour'


class BurstRateThrottle(AnonRateThrottle):
    """
    Burst protection - very short term limit
    - 2 requests per minute
    """
    scope = 'burst'
    rate = '2/min'


class LoginRateThrottle(AnonRateThrottle):
    """
    Limit login attempts to prevent brute force
    - 5 attempts per hour
    """
    scope = 'login'
    rate = '5/hour'


class LoginDailyThrottle(AnonRateThrottle):
    """
    Daily limit for login attempts
    - 20 attempts per day
    """
    scope = 'login_daily'
    rate = '20/day'
