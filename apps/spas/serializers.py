from rest_framework import serializers
from apps.location.models import State, City, Area
from .models import SpaOwner, Spa


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


class SpaOwnerSerializer(serializers.ModelSerializer):
    parent_owner_name = serializers.CharField(source='parent_owner.fullname', read_only=True)

    class Meta:
        model = SpaOwner
        fields = ['id', 'fullname', 'parent_owner', 'parent_owner_name', 'created_at', 'updated_at']


class SpaListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.fullname', read_only=True)
    state = serializers.CharField(source='area.city.state.name', read_only=True)
    city = serializers.CharField(source='area.city.name', read_only=True)
    area_name = serializers.CharField(source='area.name', read_only=True)

    class Meta:
        model = Spa
        fields = [
            'id', 'spa_code', 'spa_name', 'owner', 'owner_name',
            'status', 'state', 'city', 'area', 'area_name', 'created_at'
        ]


class SpaDetailSerializer(serializers.ModelSerializer):
    owner = SpaOwnerSerializer(read_only=True)
    sub_owners = SpaOwnerSerializer(many=True, read_only=True)
    area = AreaSerializer(read_only=True)

    class Meta:
        model = Spa
        fields = [
            'id', 'spa_code', 'spa_name', 'owner', 'sub_owners',
            'opening_date', 'reopen_date', 'status', 'line_track', 'landmark',
            'emails', 'phones', 'address', 'agreement_status', 'remark',
            'area', 'created_at', 'created_by'
        ]


class SpaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spa
        fields = [
            'spa_code', 'spa_name', 'owner', 'sub_owners', 'opening_date', 'reopen_date',
            'status', 'line_track', 'landmark', 'emails', 'phones', 'address',
            'agreement_status', 'remark', 'area'
        ]

