from rest_framework import serializers
from .models import Machine, AccountHolder


class AccountHolderSerializer(serializers.ModelSerializer):
    """Serializer for Account Holders"""
    class Meta:
        model = AccountHolder
        fields = ['id', 'full_name', 'designation', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MachineListSerializer(serializers.ModelSerializer):
    """Serializer for listing machines (location inherited from spa)"""
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_landmark = serializers.CharField(source='spa.landmark', read_only=True)
    area = serializers.IntegerField(source='area.id', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    acc_holder_name = serializers.CharField(source='acc_holder.full_name', read_only=True)
    acc_holder_designation = serializers.CharField(source='acc_holder.designation', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Machine
        fields = [
            'id', 'serial_number', 'machine_code', 'machine_name', 'model_name',
            'spa', 'spa_name', 'spa_code', 'spa_landmark',
            'area', 'area_name', 'city_name', 'state_name',
            'status', 'mid', 'tid', 'bank_name', 'account_name',
            'acc_holder', 'acc_holder_name', 'acc_holder_designation',
            'created_at', 'updated_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'area', 'area_name', 'city_name', 'state_name']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.email
        return None


class MachineDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed machine view (location inherited from spa)"""
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_landmark = serializers.CharField(source='spa.landmark', read_only=True)
    area = serializers.IntegerField(source='area.id', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    acc_holder_details = AccountHolderSerializer(source='acc_holder', read_only=True)
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Machine
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'area', 'area_name', 'city_name', 'state_name']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip() or obj.created_by.email
        return None


class MachineCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating machines (location inherited from spa)"""
    
    class Meta:
        model = Machine
        fields = [
            'serial_number', 'machine_code', 'machine_name', 'model_name', 'firmware_version',
            'spa',
            'account_name', 'bank_name', 'account_number', 'acc_holder', 'mid', 'tid',
            'status', 'remark'
        ]
    
    def validate_serial_number(self, value):
        """Ensure serial number is unique (only if provided)"""
        # Allow empty/null serial numbers
        if not value:
            return value
            
        instance_id = self.instance.id if self.instance else None
        if Machine.objects.filter(serial_number=value).exclude(id=instance_id).exists():
            raise serializers.ValidationError("Machine with this serial number already exists.")
        return value
    
    def validate_spa(self, value):
        """Validate that spa has a location assigned"""
        if value and not value.area:
            raise serializers.ValidationError(
                f"The selected spa '{value.spa_name}' does not have a location (area) assigned. "
                "Please assign a location to the spa first."
            )
        return value