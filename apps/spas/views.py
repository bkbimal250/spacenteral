from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import PrimaryOwner, SecondaryOwner, ThirdOwner, FourthOwner, Spa, SpaManager
from .filters import SpaFilter, PrimaryOwnerFilter, SecondaryOwnerFilter, ThirdOwnerFilter, FourthOwnerFilter, SpaManagerFilter
from .serializers import (
    PrimaryOwnerSerializer,
    SecondaryOwnerSerializer,
    ThirdOwnerSerializer,
    FourthOwnerSerializer,
    SpaListSerializer,
    SpaDetailSerializer,
    SpaCreateUpdateSerializer,
    SpaManagerSerializer,
    SpaManagerListSerializer,
    SpaManagerCreateUpdateSerializer,
)


class PrimaryOwnerViewSet(viewsets.ModelViewSet):
    queryset = PrimaryOwner.objects.prefetch_related('documents').all()
    serializer_class = PrimaryOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PrimaryOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class SecondaryOwnerViewSet(viewsets.ModelViewSet):
    queryset = SecondaryOwner.objects.prefetch_related('documents').all()
    serializer_class = SecondaryOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SecondaryOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class ThirdOwnerViewSet(viewsets.ModelViewSet):
    queryset = ThirdOwner.objects.prefetch_related('documents').all()
    serializer_class = ThirdOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ThirdOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class FourthOwnerViewSet(viewsets.ModelViewSet):
    queryset = FourthOwner.objects.prefetch_related('documents').all()
    serializer_class = FourthOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FourthOwnerFilter
    search_fields = ['fullname', 'email', 'phone']
    ordering_fields = ['fullname', 'created_at']
    ordering = ['fullname']


class SpaViewSet(viewsets.ModelViewSet):
    queryset = Spa.objects.select_related(
        'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'area__city__state', 'created_by'
    ).all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SpaFilter
    search_fields = [
        'spa_name', 'spa_code', 'spamanager',
        'primary_owner__fullname', 'secondary_owner__fullname',
        'third_owner__fullname', 'fourth_owner__fullname',
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
        from django.db.models import Count, Q
        
        # Get status counts
        by_status = dict(self.queryset.values('status').annotate(count=Count('id')).values_list('status', 'count'))
        
        # Get agreement status counts
        by_agreement = dict(self.queryset.values('agreement_status').annotate(count=Count('id')).values_list('agreement_status', 'count'))
        
        # Build stats in the format frontend expects
        stats = {
            'total_spas': self.queryset.count(),
            'open_spas': by_status.get('Open', 0),
            'closed_spas': by_status.get('Closed', 0),
            'temp_closed_spas': by_status.get('Temporarily Closed', 0),  # Fixed: Use correct status name
            'processing_spas': by_status.get('Processing', 0),
            'done_agreements': by_agreement.get('done', 0),
            'pending_agreements': by_agreement.get('pending', 0),
            'with_primary_owner': self.queryset.filter(primary_owner__isnull=False).count(),
            'with_secondary_owner': self.queryset.filter(secondary_owner__isnull=False).count(),
            'with_third_owner': self.queryset.filter(third_owner__isnull=False).count(),
            'with_fourth_owner': self.queryset.filter(fourth_owner__isnull=False).count(),
        }
        return Response(stats)


class SpaManagerViewSet(viewsets.ModelViewSet):
    queryset = SpaManager.objects.select_related(
        'spa', 'spa__area', 'spa__area__city', 'spa__area__city__state'
    ).prefetch_related('documents').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SpaManagerFilter
    search_fields = ['fullname', 'email', 'phone', 'spa__spa_name', 'spa__spa_code']
    ordering_fields = ['fullname', 'created_at', 'updated_at']
    ordering = ['fullname']

    def get_serializer_class(self):
        if self.action == 'list':
            return SpaManagerListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SpaManagerCreateUpdateSerializer
        return SpaManagerSerializer
    
    @action(detail=False, methods=['get'])
    def by_spa(self, request):
        """Get all managers for a specific spa"""
        spa_id = request.query_params.get('spa_id')
        if not spa_id:
            return Response({'error': 'spa_id parameter required'}, status=400)
        
        managers = self.queryset.filter(spa_id=spa_id)
        serializer = self.get_serializer(managers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get spa manager statistics"""
        from django.db.models import Count
        
        total_managers = self.queryset.count()
        managers_with_spa = self.queryset.filter(spa__isnull=False).count()
        managers_without_spa = self.queryset.filter(spa__isnull=True).count()
        
        # Managers by spa
        by_spa = self.queryset.values(
            'spa__spa_name', 'spa__spa_code'
        ).annotate(
            manager_count=Count('id')
        ).order_by('-manager_count')[:10]
        
        return Response({
            'total_managers': total_managers,
            'managers_with_spa': managers_with_spa,
            'managers_without_spa': managers_without_spa,
            'top_spas_by_manager_count': list(by_spa)
        })

# Create your views here.
