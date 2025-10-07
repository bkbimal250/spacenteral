from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DocumentType, Document
from .serializers import DocumentTypeSerializer, DocumentSerializer
from .filters import DocumentFilter


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('user', 'doc_type', 'uploaded_by').all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = ['title', 'user__email']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

# Create your views here.
