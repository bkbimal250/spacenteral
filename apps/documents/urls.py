from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTypeViewSet, DocumentViewSet, OwnerDocumentViewSet, SpaManagerDocumentViewSet

router = DefaultRouter()
router.register(r'document-types', DocumentTypeViewSet, basename='document-type')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'owner-documents', OwnerDocumentViewSet, basename='owner-document')
router.register(r'spa-manager-documents', SpaManagerDocumentViewSet, basename='spa-manager-document')

urlpatterns = [
    path('', include(router.urls)),
]


