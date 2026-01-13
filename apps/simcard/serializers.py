from rest_framework import serializers
from .models import SimCard


class SimCardSerializer(serializers.ModelSerializer):
    """Serializer for SimCard model"""

    # Spa details
    spa_name = serializers.SerializerMethodField()
    spa_code = serializers.SerializerMethodField()
    spa_address = serializers.SerializerMethodField()

    # Location details (safe nested access)
    area_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()

    # User display names
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()

    # Status display
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    class Meta:
        model = SimCard
        fields = [
            'id',

            'date_of_issue',
            'mobile_number',
            'simcard_serial_number',
            'sim_owner_name',

            'status',
            'status_display',

            'spa',
            'spa_name',
            'spa_code',
            'spa_address',

            'area_name',
            'city_name',
            'state_name',

            'created_by',
            'created_by_name',
            'updated_by',
            'updated_by_name',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

    def get_created_by_name(self, obj):
        if obj.created_by:
            full_name = f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
            return full_name or obj.created_by.email
        return None

    def get_updated_by_name(self, obj):
        if obj.updated_by:
            full_name = f"{obj.updated_by.first_name} {obj.updated_by.last_name}".strip()
            return full_name or obj.updated_by.email
        return None

    def get_spa_name(self, obj):
        return obj.spa.spa_name if obj.spa else None

    def get_spa_code(self, obj):
        return obj.spa.spa_code if obj.spa else None

    def get_spa_address(self, obj):
        return obj.spa.address if obj.spa else None

    def get_area_name(self, obj):
        return obj.spa.area.name if obj.spa and obj.spa.area else None

    def get_city_name(self, obj):
        return obj.spa.area.city.name if obj.spa and obj.spa.area and obj.spa.area.city else None

    def get_state_name(self, obj):
        return obj.spa.area.city.state.name if obj.spa and obj.spa.area and obj.spa.area.city and obj.spa.area.city.state else None
