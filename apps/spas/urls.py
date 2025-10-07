from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpaOwnerViewSet, SpaViewSet

router = DefaultRouter()
router.register(r'spa-owners', SpaOwnerViewSet, basename='spa-owner')
router.register(r'spas', SpaViewSet, basename='spa')

urlpatterns = [
    path('', include(router.urls)),
]


