from rest_framework import serializers
from django.db import models
from .models import State, City, Area


class StateSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    
    class Meta:
        model = State
        fields = ['id', 'name', 'spa_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'spa_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        """Count spas in this state through cities and areas"""
        return obj.cities.aggregate(
            total_spas=models.Count('areas__spas', distinct=True)
        )['total_spas'] or 0


class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    spa_count = serializers.SerializerMethodField()
    
    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'state_name', 'spa_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'spa_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        """Count spas in this city through areas"""
        return obj.areas.aggregate(
            total_spas=models.Count('spas', distinct=True)
        )['total_spas'] or 0


class AreaSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='city.state.name', read_only=True)
    spa_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Area
        fields = ['id', 'name', 'city', 'city_name', 'state_name', 'spa_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'spa_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        """Count spas in this area"""
        return obj.spas.count()

