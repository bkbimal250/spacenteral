"""
URL configuration for spa_central project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from apps.views import home, custom_404, custom_500

urlpatterns = [
    # Homepage
    path('', home, name='home'),
    
    # Admin
    path('admin-panel/dishaonlinesolution/', admin.site.urls),
    
    # API Authentication & Users
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.spas.urls')),
    path('api/', include('apps.machine.urls')),
    path('api/', include('apps.documents.urls')),
    path('api/', include('apps.location.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.simcard.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/', include('rest_framework.urls')),
    
    # Health check
    path('health/', lambda request: __import__('django.http').HttpResponse('OK'), name='health_check'),
]

# Custom error handlers
handler404 = custom_404
handler500 = custom_500

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
