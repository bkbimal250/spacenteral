from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import State, City, Area
from .serializers import StateSerializer, CitySerializer, AreaSerializer


class StateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing States
    """
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get location statistics with spa counts"""
        total_states = State.objects.count()
        total_cities = City.objects.count()
        total_areas = Area.objects.count()
        
        # Get total spa count across all locations
        from apps.spas.models import Spa
        total_spas = Spa.objects.count()
        
        # States with most cities and spas
        states_with_stats = State.objects.annotate(
            city_count=Count('cities'),
            spa_count=Count('cities__areas__spas', distinct=True)
        ).order_by('-city_count')[:5]
        
        # Cities with most areas and spas
        cities_with_stats = City.objects.annotate(
            area_count=Count('areas'),
            spa_count=Count('areas__spas', distinct=True)
        ).select_related('state').order_by('-area_count')[:5]
        
        # Areas with most spas
        areas_with_spas = Area.objects.annotate(
            spa_count=Count('spas')
        ).select_related('city', 'city__state').order_by('-spa_count')[:5]
        
        # Recent additions
        recent_states = State.objects.order_by('-created_at')[:5]
        recent_cities = City.objects.select_related('state').order_by('-created_at')[:5]
        recent_areas = Area.objects.select_related('city', 'city__state').order_by('-created_at')[:5]
        
        return Response({
            'totals': {
                'states': total_states,
                'cities': total_cities,
                'areas': total_areas,
                'spas': total_spas,
            },
            'top_states': [
                {
                    'id': s.id,
                    'name': s.name,
                    'city_count': s.city_count,
                    'spa_count': s.spa_count
                }
                for s in states_with_stats
            ],
            'top_cities': [
                {
                    'id': c.id,
                    'name': c.name,
                    'state_name': c.state.name,
                    'area_count': c.area_count,
                    'spa_count': c.spa_count
                }
                for c in cities_with_stats
            ],
            'top_areas': [
                {
                    'id': a.id,
                    'name': a.name,
                    'city_name': a.city.name,
                    'state_name': a.city.state.name,
                    'spa_count': a.spa_count
                }
                for a in areas_with_spas
            ],
            'recent': {
                'states': StateSerializer(recent_states, many=True).data,
                'cities': CitySerializer(recent_cities, many=True).data,
                'areas': AreaSerializer(recent_areas, many=True).data,
            }
        })


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Cities
    """
    queryset = City.objects.select_related('state').all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state']
    search_fields = ['name', 'state__name']
    ordering_fields = ['name', 'created_at']
    ordering = ['state', 'name']


class AreaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Areas
    """
    queryset = Area.objects.select_related('city', 'city__state').all()
    serializer_class = AreaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'city__state']
    search_fields = ['name', 'city__name', 'city__state__name']
    ordering_fields = ['name', 'created_at']
    ordering = ['city', 'name']
