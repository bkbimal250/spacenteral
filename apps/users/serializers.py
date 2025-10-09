from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from .models import User, UserProfile, OTP
from .utils import create_otp, send_otp_email, verify_otp, get_or_create_user_by_email


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'preferences', 'notification_settings']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'user_type', 'phone', 'profile_picture', 'date_of_birth',
            'address', 'is_verified', 'is_active', 'created_at', 'updated_at', 'profile'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'updated_at', 'is_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2',
            'first_name', 'last_name', 'user_type', 'phone'
        ]
    
    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Create user with email as the username field
        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data.get('user_type', 'employee'),
            phone=validated_data.get('phone', '')
        )
        UserProfile.objects.create(user=user)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'profile_picture',
            'date_of_birth', 'address'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class RequestOTPSerializer(serializers.Serializer):
    """Serializer for requesting OTP"""
    
    email = serializers.EmailField(required=True)
    purpose = serializers.ChoiceField(
        choices=['login', 'registration', 'password_reset'],
        default='login'
    )
    
    def validate_email(self, value):
        """Validate email"""
        return value.lower()
    
    def validate(self, attrs):
        email = attrs['email']
        purpose = attrs.get('purpose', 'login')
        
        # For login and password_reset, user must exist
        if purpose in ['login', 'password_reset']:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    "email": "No user found with this email address."
                })
        
        return attrs
    
    def save(self):
        """Generate and send OTP"""
        email = self.validated_data['email']
        purpose = self.validated_data.get('purpose', 'login')
        
        # Get or create user
        if purpose == 'registration':
            user, created = get_or_create_user_by_email(
                email=email,
                first_name='',
                last_name='',
                user_type='employee'
            )
        else:
            user = User.objects.get(email=email)
        
        # Create OTP
        otp = create_otp(user, purpose=purpose)
        
        # Send OTP via email
        email_sent = send_otp_email(user, otp, purpose=purpose)
        
        if not email_sent:
            raise serializers.ValidationError({
                "email": "Failed to send OTP. Please try again."
            })
        
        return {
            'email': user.email,
            'message': f'OTP sent to {user.email}',
            'expires_in_minutes': 10
        }


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying OTP and logging in"""
    
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    purpose = serializers.ChoiceField(
        choices=['login', 'registration', 'password_reset'],
        default='login'
    )
    
    # Optional fields for registration
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    phone = serializers.CharField(required=False, max_length=20)
    
    def validate_email(self, value):
        """Validate email"""
        return value.lower()
    
    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        purpose = attrs.get('purpose', 'login')
        
        # Verify OTP
        success, message, user = verify_otp(email, code, purpose)
        
        if not success:
            raise serializers.ValidationError({"code": message})
        
        attrs['user'] = user
        return attrs
    
    def save(self):
        """Process OTP verification"""
        user = self.validated_data['user']
        purpose = self.validated_data.get('purpose', 'login')
        
        # Update user details if provided (for registration)
        if purpose == 'registration':
            if self.validated_data.get('first_name'):
                user.first_name = self.validated_data['first_name']
            if self.validated_data.get('last_name'):
                user.last_name = self.validated_data['last_name']
            if self.validated_data.get('phone'):
                user.phone = self.validated_data['phone']
            
            user.is_verified = True
            user.save()
            
            # Create user profile if doesn't exist
            UserProfile.objects.get_or_create(user=user)
        
        # Generate or get auth token
        token, created = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }


class OTPSerializer(serializers.ModelSerializer):
    """Serializer for OTP model (admin use)"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = OTP
        fields = [
            'id', 'user', 'user_email', 'code', 'purpose',
            'is_used', 'is_valid', 'expires_at', 'created_at', 'used_at'
        ]
        read_only_fields = ['id', 'created_at', 'used_at']
    
    def get_is_valid(self, obj):
        return obj.is_valid()


class EmailPasswordLoginSerializer(serializers.Serializer):
    """Serializer for traditional email/password login"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate_email(self, value):
        """Normalize email to lowercase"""
        return value.lower()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        # Try to authenticate user
        from django.contrib.auth import authenticate
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError({
                "detail": "Invalid email or password."
            })
        
        if not user.is_active:
            raise serializers.ValidationError({
                "detail": "User account is disabled."
            })
        
        attrs['user'] = user
        return attrs
    
    def save(self):
        """Return user data and token"""
        user = self.validated_data['user']
        
        # Generate or get auth token
        token, created = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }


class ResetPasswordViaOTPSerializer(serializers.Serializer):
    """Reset password by verifying OTP without knowing old password"""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': "Password fields didn't match."})

        # verify OTP for password_reset purpose
        success, message, user = verify_otp(attrs['email'], attrs['code'], 'password_reset')
        if not success:
            raise serializers.ValidationError({'code': message})

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.is_verified = True
        user.save(update_fields=['password', 'is_verified'])

        # issue token for immediate login
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Password reset successful'
        }

