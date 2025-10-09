from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.http import FileResponse
from .models import DocumentType, Document
from .serializers import (
    DocumentTypeSerializer, 
    DocumentListSerializer,
    DocumentDetailSerializer,
    DocumentCreateUpdateSerializer
)
from .filters import DocumentFilter


class DocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for document types - only admin can create/edit/delete via Django admin
    """
    queryset = DocumentType.objects.filter(is_active=True)  # Only show active types
    serializer_class = DocumentTypeSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('doc_type', 'uploaded_by', 'spa').all()
    # Public: anyone can list, upload, and download
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DocumentFilter
    search_fields = ['title', 'notes', 'spa_code', 'spa_name', 'doc_type__name']
    ordering_fields = ['created_at', 'title', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DocumentCreateUpdateSerializer
        return DocumentDetailSerializer

    def perform_create(self, serializer):
        uploader = self.request.user if getattr(self.request, 'user', None) and self.request.user.is_authenticated else None
        serializer.save(uploaded_by=uploader)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get document statistics"""
        total_docs = self.queryset.count()
        by_type = dict(self.queryset.values('doc_type__name').annotate(
            count=Count('id')
        ).values_list('doc_type__name', 'count'))
        
        by_user = self.queryset.values('user__email').annotate(
            count=Count('id')
        ).order_by('-count')[:10]  # Top 10 users
        
        by_uploader = self.queryset.values('uploaded_by__email').annotate(
            count=Count('id')
        ).order_by('-count')[:10]  # Top 10 uploaders
        
        return Response({
            'total_documents': total_docs,
            'by_document_type': by_type,
            'top_users_with_documents': list(by_user),
            'top_uploaders': list(by_uploader)
        })
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a document file"""
        document = self.get_object()
        if document.file:
            return FileResponse(
                document.file.open('rb'),
                as_attachment=True,
                filename=document.file.name.split('/')[-1]
            )
        return Response(
            {'error': 'No file attached'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Deprecated user-specific endpoints removed for public model
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get documents by type"""
        doc_type_id = request.query_params.get('doc_type')
        if not doc_type_id:
            return Response({'error': 'doc_type parameter required'}, status=400)
        
        docs = self.queryset.filter(doc_type_id=doc_type_id)
        serializer = self.get_serializer(docs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get documents for a specific user"""
        user_id = request.query_params.get('user')
        if not user_id:
            return Response({'error': 'user parameter required'}, status=400)
        
        docs = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(docs, many=True)
        return Response(serializer.data)

# Create your views here.
