from rest_framework import serializers
from apps.location.models import State, City, Area
from .models import PrimaryOwner, SecondaryOwner, ThirdOwner, FourthOwner, Spa, SpaManager,SocialMediaLink,SpaWebsite, SpaMedia


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
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PrimaryOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'document_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class SecondaryOwnerSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SecondaryOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'document_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class ThirdOwnerSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ThirdOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'document_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class FourthOwnerSerializer(serializers.ModelSerializer):
    spa_count = serializers.SerializerMethodField()
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = FourthOwner
        fields = ['id', 'fullname', 'email', 'phone', 'spa_count', 'document_count', 'created_at', 'updated_at']
    
    def get_spa_count(self, obj):
        return obj.spas.count()
    
    def get_document_count(self, obj):
        return obj.documents.count()


class SpaListSerializer(serializers.ModelSerializer):
    primary_owner_name = serializers.CharField(source='primary_owner.fullname', read_only=True)
    secondary_owner_name = serializers.CharField(source='secondary_owner.fullname', read_only=True)
    third_owner_name = serializers.CharField(source='third_owner.fullname', read_only=True)
    fourth_owner_name = serializers.CharField(source='fourth_owner.fullname', read_only=True)
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
            'third_owner', 'third_owner_name',
            'fourth_owner', 'fourth_owner_name',
            'spamanager', 'status', 'agreement_status', 'agreement_status_display',
            'state', 'city', 'area', 'area_name', 'google_map_link', 'google_drive_link', 'created_at'
        ]


class SpaDetailSerializer(serializers.ModelSerializer):
    primary_owner = PrimaryOwnerSerializer(read_only=True)
    secondary_owner = SecondaryOwnerSerializer(read_only=True)
    third_owner = ThirdOwnerSerializer(read_only=True)
    fourth_owner = FourthOwnerSerializer(read_only=True)
    area = AreaSerializer(read_only=True)
    agreement_status_display = serializers.CharField(source='get_agreement_status_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Spa
        fields = [
            'id', 'spa_code', 'spa_name', 
            'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'spamanager',
            'opening_date', 
            'status', 'status_display',
            'line_track', 'landmark',
            'emails', 'phones', 'address', 'google_map_link', 'google_drive_link',
            'agreement_status', 'agreement_status_display', 'remark',
            'area', 'created_at', 'created_by'
        ]


class SpaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = [
            'spa_code', 'spa_name', 
            'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'spamanager',
            'opening_date',
            'status', 'line_track', 'landmark', 
            'emails', 'phones', 'address', 'google_map_link', 'google_drive_link',
            'agreement_status', 'remark', 'area'
        ]
    
    def validate(self, data):
        # Ensure at least primary owner is provided
        if not data.get('primary_owner'):
            raise serializers.ValidationError({
                'primary_owner': 'Primary owner is required'
            })
        return data


class SpaManagerSerializer(serializers.ModelSerializer):
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SpaManager
        fields = [
            'id', 'fullname', 'email', 'phone', 'address',
            'spa', 'spa_name', 'spa_code',
            'area_name', 'city_name', 'state_name',
            'document_count',
            'created_at', 'updated_at'
        ]
    
    def get_document_count(self, obj):
        return obj.documents.count()


class SpaManagerListSerializer(serializers.ModelSerializer):
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SpaManager
        fields = [
            'id', 'fullname', 'email', 'phone', 'address',
            'spa', 'spa_name', 'spa_code',
            'area_name', 'city_name', 'state_name',
            'document_count',
            'created_at'
        ]
    
    def get_document_count(self, obj):
        return obj.documents.count()


class SpaManagerCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaManager
        fields = ['fullname', 'email', 'phone', 'address', 'spa']
    
    def validate(self, data):
        # Optional: Add any custom validation if needed
        return data


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_address = serializers.CharField(source='spa.address', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    
    class Meta:
        model = SocialMediaLink
        fields = ['id', 'spa', 'spa_name', 'spa_code', 'spa_address', 'area_name', 'city_name', 'state_name', 'platform', 'url', 'created_at', 'updated_at']


class SpaWebsiteLinkSerializer(serializers.ModelSerializer):
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_address = serializers.CharField(source='spa.address', read_only=True)

    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)

    class Meta:
        model = SpaWebsite      # ✅ FIXED
        fields = [
            'id', 
            'spa', 
            'spa_name', 'spa_code', 'spa_address',
            'area_name', 'city_name', 'state_name',
            'category', 'url',
            'created_at', 'updated_at'
        ]


class SpaMediaSerializer(serializers.ModelSerializer):
    """Serializer for SpaMedia with spa details"""
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_address = serializers.CharField(source='spa.address', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = SpaMedia
        fields = [
            'id',
            'spa', 'spa_name', 'spa_code', 'spa_address',
            'area_name', 'city_name', 'state_name',
            'url',
            'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]


class SpaMediaListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for SpaMedia list view"""
    spa_name = serializers.CharField(source='spa.spa_name', read_only=True)
    spa_code = serializers.CharField(source='spa.spa_code', read_only=True)
    spa_address = serializers.CharField(source='spa.address', read_only=True)
    area_name = serializers.CharField(source='spa.area.name', read_only=True)
    city_name = serializers.CharField(source='spa.area.city.name', read_only=True)
    state_name = serializers.CharField(source='spa.area.city.state.name', read_only=True)
    
    class Meta:
        model = SpaMedia
        fields = [
            'id',
            'spa', 'spa_name', 'spa_code', 'spa_address',
            'area_name', 'city_name', 'state_name',
            'url',
            'created_at'
        ]


class SpaMediaCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating SpaMedia"""
    
    class Meta:
        model = SpaMedia
        fields = ['spa', 'url']
    
    def validate(self, data):
        # Optional: Add validation if needed
        return data
