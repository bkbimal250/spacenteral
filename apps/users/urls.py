from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, RequestOTPView,
    VerifyOTPView, OTPViewSet, EmailPasswordLoginView,
    RequestPasswordResetOTPView, ResetPasswordViaOTPView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'otps', OTPViewSet, basename='otp')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', EmailPasswordLoginView.as_view(), name='email-password-login'),
    path('auth/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('auth/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('auth/request-password-reset-otp/', RequestPasswordResetOTPView.as_view(), name='request-password-reset-otp'),
    path('auth/reset-password/', ResetPasswordViaOTPView.as_view(), name='reset-password-via-otp'),
    
    # Other user endpoints
    path('', include(router.urls)),
]

