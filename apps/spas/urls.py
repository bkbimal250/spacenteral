from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrimaryOwnerViewSet, SecondaryOwnerViewSet, SpaViewSet

router = DefaultRouter()
router.register(r'primary-owners', PrimaryOwnerViewSet, basename='primary-owner')
router.register(r'secondary-owners', SecondaryOwnerViewSet, basename='secondary-owner')
router.register(r'spas', SpaViewSet, basename='spa')

urlpatterns = [
    path('', include(router.urls)),
]


