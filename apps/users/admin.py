from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_staff', 'created_at']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_active']
    search_fields = ['email', 'phone', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'address')}),
        ('Profile', {'fields': ('profile_picture', 'user_type', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type', 'phone'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
    
    def created_at(self, obj):
        return obj.user.created_at
    created_at.short_description = 'Created At'


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = [
        'user_email', 'code_display', 'purpose', 'is_valid_display',
        'is_used', 'created_at', 'expires_at'
    ]
    list_filter = ['purpose', 'is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['created_at', 'used_at', 'code', 'expires_at']
    raw_id_fields = ['user']
    
    fieldsets = (
        ('User & Code', {
            'fields': ('user', 'code', 'purpose')
        }),
        ('Status', {
            'fields': ('is_used', 'expires_at', 'used_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def code_display(self, obj):
        """Display code with masking for security"""
        if obj.is_used:
            return f"***{obj.code[-3:]}"
        return obj.code
    code_display.short_description = 'Code'
    
    def is_valid_display(self, obj):
        """Display validity status with color"""
        is_valid = obj.is_valid()
        if is_valid:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Valid</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Expired/Used</span>'
            )
    is_valid_display.short_description = 'Valid'
    
    def has_add_permission(self, request):
        """Prevent manual OTP creation through admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent OTP modification through admin"""
        return False

