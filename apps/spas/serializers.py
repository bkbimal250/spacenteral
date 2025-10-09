from rest_framework import serializers
from apps.location.models import State, City, Area
from .models import PrimaryOwner, SecondaryOwner, Spa


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'state']


class AreaSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'city']


class PrimaryOwnerSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PrimaryOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()


class SecondaryOwnerSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SecondaryOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()


class SpaListSerializer(serializers.ModelSerializer):
    primary_owner_name = serializers.CharField(source='primary_owner.fullname', read_only=True)
    secondary_owner_name = serializers.CharField(source='secondary_owner.fullname', read_only=True)
    state = serializers.CharField(source='area.city.state.name', read_only=True)
    city = serializers.CharField(source='area.city.name', read_only=True)
    area_name = serializers.CharField(source='area.name', read_only=True)
    agreement_status_display = serializers.CharField(source='get_agreement_status_display', read_only=True)

    class Meta:
        model = Spa
        fields = [
            'id', 'spa_code', 'spa_name', 
            'primary_owner', 'primary_owner_name',
            'secondary_owner', 'secondary_owner_name',
            'spamanager', 'status', 'agreement_status', 'agreement_status_display',
            'state', 'city', 'area', 'area_name', 'google_map_link', 'created_at'
        ]


class SpaDetailSerializer(serializers.ModelSerializer):
    primary_owner = PrimaryOwnerSerializer(read_only=True)
    secondary_owner = SecondaryOwnerSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    agreement_status_display = serializers.CharField(source='get_agreement_status_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Spa
        fields = [
            'id', 'spa_code', 'spa_name', 
            'primary_owner', 'secondary_owner', 'spamanager',
            'opening_date', 
            'status', 'status_display',
            'line_track', 'landmark',
            'emails', 'phones', 'address', 'google_map_link',
            'agreement_status', 'agreement_status_display', 'remark',
            'area', 'created_at', 'created_by'
        ]


class SpaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = [
            'spa_code', 'spa_name', 
            'primary_owner', 'secondary_owner', 'spamanager',
            'opening_date',
            'status', 'line_track', 'landmark', 
            'emails', 'phones', 'address', 'google_map_link',
            'agreement_status', 'remark', 'area'
        ]
    
    def validate(self, data):
        # Ensure at least primary owner is provided
        if not data.get('primary_owner'):
            raise serializers.ValidationError({
                'primary_owner': 'Primary owner is required'
            })
        return data

