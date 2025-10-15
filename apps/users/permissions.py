"""
Custom permissions for the application
"""
from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Permission class to allow admin, manager, and spa_manager users.
    Used to protect dashboard endpoints.
    Note: spa_manager is also known as area_manager
    """
    message = "Access denied. Only administrators, managers, or spa managers can access this resource."

    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow admin, manager, and spa_manager (area_manager)
        return request.user.user_type in ['admin', 'manager', 'spa_manager']


class IsAdminOnly(BasePermission):
    """
    Permission class to allow ONLY admin users (strict).
    Used for sensitive operations like user management.
    """
    message = "Access denied. Only administrators can access this resource."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_type == 'admin'


class IsSpaManager(BasePermission):
    """
    Permission class to allow only spa managers (area managers).
    """
    message = "Access denied. Only spa managers can access this resource."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_type == 'spa_manager'


class IsManager(BasePermission):
    """
    Permission class to allow only managers.
    """
    message = "Access denied. Only managers can access this resource."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.user_type == 'manager'


class IsOwnerOrAdmin(BasePermission):
    """
    Permission to allow only admins or the owner of an object.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Admin can access anything
        if request.user.user_type == 'admin':
            return True
        
        # Check if object has user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object is the user itself
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow admins/managers to edit.
    Other authenticated users have read-only access.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user and request.user.is_authenticated
        
        # Write permissions for admin, manager, and spa_manager
        return (request.user and request.user.is_authenticated and 
                request.user.user_type in ['admin', 'manager', 'spa_manager'])

