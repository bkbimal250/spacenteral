from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTypeViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet, basename='document-type')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]


