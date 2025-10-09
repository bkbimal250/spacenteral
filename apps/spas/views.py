from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import PrimaryOwner, SecondaryOwner, Spa
from .filters import SpaFilter, PrimaryOwnerFilter, SecondaryOwnerFilter
from .serializers import (
    PrimaryOwnerSerializer,
    SecondaryOwnerSerializer,
    SpaListSerializer,
    SpaDetailSerializer,
    SpaCreateUpdateSerializer,
)


class PrimaryOwnerViewSet(viewsets.ModelViewSet):
    queryset = PrimaryOwner.objects.all()
    serializer_class = PrimaryOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PrimaryOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class SecondaryOwnerViewSet(viewsets.ModelViewSet):
    queryset = SecondaryOwner.objects.all()
    serializer_class = SecondaryOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SecondaryOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class SpaViewSet(viewsets.ModelViewSet):
    queryset = Spa.objects.select_related(
        'primary_owner', 'secondary_owner', 'area__city__state', 'created_by'
    ).all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SpaFilter
    search_fields = [
        'spa_name', 'spa_code', 'spamanager',
        'primary_owner__fullname', 'secondary_owner__fullname',
        'emails', 'phones', 'address'
    ]
    ordering_fields = ['spa_name', 'spa_code', 'created_at', 'opening_date', 'status']
    ordering = ['spa_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return SpaListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SpaCreateUpdateSerializer
        return SpaDetailSerializer
    
    def perform_create(self, serializer):
        """Auto-assign created_by when creating spa"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get spas grouped by status"""
        status_param = request.query_params.get('status')
        if status_param:
            spas = self.queryset.filter(status=status_param)
            serializer = self.get_serializer(spas, many=True)
            return Response(serializer.data)
        return Response({'error': 'Status parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def by_agreement(self, request):
        """Get spas grouped by agreement status"""
        agreement = request.query_params.get('agreement_status')
        if agreement:
            spas = self.queryset.filter(agreement_status=agreement)
            serializer = self.get_serializer(spas, many=True)
            return Response(serializer.data)
        return Response({'error': 'agreement_status parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get spa statistics"""
        from django.db.models import Count
        
        stats = {
            'total': self.queryset.count(),
            'by_status': dict(self.queryset.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_agreement': dict(self.queryset.values('agreement_status').annotate(count=Count('id')).values_list('agreement_status', 'count')),
            'with_primary_owner': self.queryset.filter(primary_owner__isnull=False).count(),
            'with_secondary_owner': self.queryset.filter(secondary_owner__isnull=False).count(),
        }
        return Response(stats)

# Create your views here.
