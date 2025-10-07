from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Machine, MachineAssignment
from .serializers import MachineSerializer, MachineAssignmentSerializer
from .filters import MachineFilter


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.select_related('spa', 'installed_area__city__state').all()
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MachineFilter
    search_fields = ['serial_number', 'model_name', 'spa__spa_name']
    ordering_fields = ['serial_number', 'created_at']
    ordering = ['serial_number']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)


class MachineAssignmentViewSet(viewsets.ModelViewSet):
    queryset = MachineAssignment.objects.select_related('machine', 'from_spa', 'to_spa').all()
    serializer_class = MachineAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['machine', 'to_spa', 'to_area']

# Create your views here.
