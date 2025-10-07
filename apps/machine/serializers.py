from rest_framework import serializers
from apps.location.models import Area
from apps.spas.models import Spa
from .models import Machine, MachineAssignment


class MachineSerializer(serializers.ModelSerializer):
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    area_name = serializers.CharField(source='installed_area.name', read_only=True)
    city = serializers.CharField(source='installed_area.city.name', read_only=True)
    state = serializers.CharField(source='installed_area.city.state.name', read_only=True)

    class Meta:
        model = Machine
        fields = [
            'id', 'serial_number', 'model_name', 'firmware_version',
            'spa', 'spa_name', 'installed_area', 'area_name', 'city', 'state',
            'ip_address', 'location_note', 'status', 'activated_at', 'last_service_date',
            'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class MachineAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineAssignment
        fields = ['id', 'machine', 'from_spa', 'to_spa', 'from_area', 'to_area', 'moved_at', 'note']
        read_only_fields = ['moved_at']

