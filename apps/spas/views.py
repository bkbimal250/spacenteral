from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import SpaOwner, Spa
from .serializers import (
    SpaOwnerSerializer,
    SpaListSerializer,
    SpaDetailSerializer,
    SpaCreateUpdateSerializer,
)


class SpaOwnerViewSet(viewsets.ModelViewSet):
    queryset = SpaOwner.objects.select_related('parent_owner').all()
    serializer_class = SpaOwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['parent_owner']
    search_fields = ['fullname', 'parent_owner__fullname']
    ordering = ['fullname']


class SpaViewSet(viewsets.ModelViewSet):
    queryset = Spa.objects.select_related('owner', 'area__city__state').prefetch_related('sub_owners').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'area', 'area__city', 'area__city__state', 'owner']
    search_fields = ['spa_name', 'spa_code', 'owner__fullname', 'emails', 'phones']
    ordering_fields = ['spa_name', 'created_at']
    ordering = ['spa_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return SpaListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return SpaCreateUpdateSerializer
        return SpaDetailSerializer

# Create your views here.
