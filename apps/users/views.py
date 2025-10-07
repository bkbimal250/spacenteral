from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash
from .models import User, UserProfile, OTP
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    UserUpdateSerializer, ChangePasswordSerializer,
    UserProfileSerializer, RequestOTPSerializer,
    VerifyOTPSerializer, OTPSerializer,
    EmailPasswordLoginSerializer, ResetPasswordViaOTPSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user profile"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(request.user).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Wrong password.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': 'Password updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def my_profile(self, request):
        """Get or update current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    """
    Request OTP for login, registration, or password reset
    
    POST /api/auth/request-otp/
    {
        "email": "user@example.com",
        "purpose": "login"  // or "registration" or "password_reset"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    Verify OTP and login/register user
    
    POST /api/auth/verify-otp/
    {
        "email": "user@example.com",
        "code": "123456",
        "purpose": "login",
        "first_name": "John",  // optional, for registration
        "last_name": "Doe",    // optional, for registration
        "phone": "+1234567890" // optional, for registration
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing OTP history (admin only)"""
    queryset = OTP.objects.select_related('user').all()
    serializer_class = OTPSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Only allow staff to see all OTPs
        if self.request.user.is_staff:
            return queryset
        # Regular users can only see their own OTPs
        return queryset.filter(user=self.request.user)


class EmailPasswordLoginView(APIView):
    """
    Traditional email/password login
    
    POST /api/auth/login/
    {
        "email": "user@example.com",
        "password": "yourpassword"
    }
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailPasswordLoginSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetOTPView(APIView):
    """Request an OTP for resetting password"""
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()
        data['purpose'] = 'password_reset'
        serializer = RequestOTPSerializer(data=data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordViaOTPView(APIView):
    """Reset password using email + otp + new password"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordViaOTPSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

