from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import SimCard
from .serializers import SimCardSerializer


class SimCardViewSet(viewsets.ModelViewSet):
    """
    CRUD API for SimCard
    """
    serializer_class = SimCardSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filters
    filterset_fields = [
        'status',
        'spa',
    ]

    # Search fields
    search_fields = [
        'mobile_number',
        'simcard_serial_number',
        'sim_owner_name',
        'spa__spa_name',
        'spa__spa_code',
    ]

    # Ordering
    ordering_fields = [
        'created_at',
        'date_of_issue',
        'mobile_number',
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optimized queryset with related data
        """
        return (
            SimCard.objects
            .select_related(
                'spa',
                'spa__area',
                'spa__area__city',
                'spa__area__city__state',
                'created_by',
                'updated_by'
            )
        )

    def perform_create(self, serializer):
        """
        Auto-assign created_by and updated_by
        """
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        """
        Auto-update updated_by
        """
        serializer.save(updated_by=self.request.user)
