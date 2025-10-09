from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Machine, AccountHolder
from .serializers import (
    MachineListSerializer,
    MachineDetailSerializer,
    MachineCreateUpdateSerializer,
    AccountHolderSerializer
)
from .filters import MachineFilter


class MachineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Machines (Card Swipe Machines)
    Complete record keeping system replacing Excel
    """
    queryset = Machine.objects.select_related(
        'spa', 'spa__area', 'spa__area__city', 'spa__area__city__state', 'created_by', 'acc_holder'
    ).all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MachineFilter
    search_fields = [
        'serial_number', 'machine_code', 'machine_name', 'model_name',
        'spa__spa_name', 'spa__spa_code', 'spa__landmark', 
        'mid', 'tid', 'bank_name', 'account_name',
        'acc_holder__full_name', 'acc_holder__designation',
        'spa__area__name', 'spa__area__city__name', 'spa__area__city__state__name'
    ]
    ordering_fields = ['serial_number', 'machine_code', 'created_at', 'status', 'spa__spa_name']
    ordering = ['spa__spa_name', 'serial_number']

    def get_serializer_class(self):
        if self.action == 'list':
            return MachineListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MachineCreateUpdateSerializer
        return MachineDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get comprehensive machine statistics"""
        total_machines = Machine.objects.count()
        total_account_holders = AccountHolder.objects.count()
        
        # Status breakdown
        status_counts = {}
        for status_code, status_label in Machine.STATUS_CHOICES:
            count = Machine.objects.filter(status=status_code).count()
            status_counts[status_code] = {
                'label': status_label,
                'count': count
            }
        
        # Account holder statistics
        account_holders_with_machines = AccountHolder.objects.annotate(
            machine_count=Count('machines')
        ).filter(machine_count__gt=0)
        
        account_holders_stats = {
            'total_account_holders': total_account_holders,
            'holders_with_machines': account_holders_with_machines.count(),
            'holders_without_machines': total_account_holders - account_holders_with_machines.count(),
            'top_holders': list(
                account_holders_with_machines.values(
                    'id', 'full_name', 'designation', 'machine_count'
                ).order_by('-machine_count')[:5]
            )
        }
        
        # Machines by location
        machines_by_state = Machine.objects.filter(
            spa__area__city__state__isnull=False
        ).values(
            'spa__area__city__state__id', 'spa__area__city__state__name'
        ).annotate(
            machine_count=Count('id')
        ).order_by('-machine_count')[:10]
        
        machines_by_spa = Machine.objects.filter(
            spa__isnull=False
        ).values(
            'spa__id', 'spa__spa_name', 'spa__spa_code'
        ).annotate(
            machine_count=Count('id')
        ).order_by('-machine_count')[:10]
        
        # Recent machines
        recent_machines = Machine.objects.select_related(
            'spa', 'spa__area', 'spa__area__city', 'spa__area__city__state', 'acc_holder'
        ).order_by('-created_at')[:5]
        
        # Machines needing service - placeholder (can be customized based on other criteria)
        needs_service_count = 0  # Can be implemented based on other business logic if needed
        
        # Machines by model
        machines_by_model = Machine.objects.filter(
            model_name__isnull=False
        ).values('model_name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Banking statistics
        banking_stats = {
            'machines_with_mid': Machine.objects.exclude(mid__isnull=True).exclude(mid='').count(),
            'machines_with_tid': Machine.objects.exclude(tid__isnull=True).exclude(tid='').count(),
            'machines_with_bank_info': Machine.objects.exclude(
                Q(account_name__isnull=True) | Q(account_name='') |
                Q(bank_name__isnull=True) | Q(bank_name='')
            ).count(),
            'machines_with_account_holder': Machine.objects.exclude(acc_holder__isnull=True).count(),
        }
        
        return Response({
            'totals': {
                'total_machines': total_machines,
                'total_account_holders': total_account_holders,
                'in_use': status_counts.get('in_use', {}).get('count', 0),
                'not_in_use': status_counts.get('not_in_use', {}).get('count', 0),
                'broken': status_counts.get('broken', {}).get('count', 0),
                'needs_service': needs_service_count,
            },
            'status_breakdown': status_counts,
            'account_holders': account_holders_stats,
            'banking': banking_stats,
            'by_state': list(machines_by_state),
            'by_spa': list(machines_by_spa),
            'by_model': list(machines_by_model),
            'recent': MachineListSerializer(recent_machines, many=True).data,
        })
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get machines filtered by status"""
        status = request.query_params.get('status')
        if not status:
            return Response({'error': 'Status parameter required'}, status=400)
        
        machines = self.get_queryset().filter(status=status)
        serializer = MachineListSerializer(machines, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_spa(self, request):
        """Get machines for a specific spa"""
        spa_id = request.query_params.get('spa_id')
        if not spa_id:
            return Response({'error': 'spa_id parameter required'}, status=400)
        
        machines = self.get_queryset().filter(spa_id=spa_id)
        serializer = MachineListSerializer(machines, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def needs_service(self, request):
        """Get machines that need service - placeholder endpoint"""
        # Can be customized based on business logic
        machines = []
        serializer = MachineListSerializer(machines, many=True)
        return Response(serializer.data)


class AccountHolderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Account Holders
    """
    queryset = AccountHolder.objects.all()
    serializer_class = AccountHolderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'designation']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']