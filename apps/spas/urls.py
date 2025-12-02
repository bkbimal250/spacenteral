from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrimaryOwnerViewSet,
    SecondaryOwnerViewSet,
    ThirdOwnerViewSet,
    FourthOwnerViewSet,
    SpaViewSet,
    SpaManagerViewSet,
    SocialMediaLinkViewSet,
    SpaWebsiteLinkViewset,
)

router = DefaultRouter()
router.register(r'primary-owners', PrimaryOwnerViewSet, basename='primary-owner')
router.register(r'secondary-owners', SecondaryOwnerViewSet, basename='secondary-owner')
router.register(r'third-owners', ThirdOwnerViewSet, basename='third-owner')
router.register(r'fourth-owners', FourthOwnerViewSet, basename='fourth-owner')
router.register(r'spas', SpaViewSet, basename='spa')
router.register(r'spa-managers', SpaManagerViewSet, basename='spa-manager')
router.register(r'social-media-links', SocialMediaLinkViewSet, basename='social-media-link')
router.register(r'spa-websites', SpaWebsiteLinkViewset, basename='spa-website')

urlpatterns = [
    path('', include(router.urls)),
]


