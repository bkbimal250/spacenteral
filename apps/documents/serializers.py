from rest_framework import serializers
from .models import DocumentType, Document, OwnerDocument
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentTypeSerializer(serializers.ModelSerializer):
    document_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'is_active', 'document_count', 'created_at', 'updated_at']
    
    def get_document_count(self, obj):
        return obj.documents.count()


class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'user_type', 'profile_picture']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email


class DocumentListSerializer(serializers.ModelSerializer):
    doc_type_name = serializers.CharField(source='doc_type.name', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'doc_type', 'doc_type_name',
            'spa', 'spa_code', 'spa_name', 'state_name', 'city_name', 'area_name',
            'uploaded_by', 'uploaded_by_name',
            'file', 'file_size', 'file_extension',
            'created_at', 'updated_at'
        ]
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}".strip() or obj.uploaded_by.email
        return "System"
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                # Convert to human readable
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
            except:
                return "Unknown"
        return "N/A"
    
    def get_file_extension(self, obj):
        if obj.file:
            return obj.file.name.split('.')[-1].upper()
        return "N/A"


class DocumentDetailSerializer(serializers.ModelSerializer):
    uploaded_by = UserBasicSerializer(read_only=True)
    doc_type = DocumentTypeSerializer(read_only=True)
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'doc_type', 'spa', 'spa_code', 'spa_name', 'state_name', 'city_name', 'area_name', 'uploaded_by',
            'file', 'file_size', 'file_extension',
            'notes', 'created_at', 'updated_at'
        ]
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
            except:
                return "Unknown"
        return "N/A"
    
    def get_file_extension(self, obj):
        if obj.file:
            return obj.file.name.split('.')[-1].upper()
        return "N/A"


class DocumentCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        fields = ['title', 'doc_type', 'spa', 'file', 'notes']
    
    def validate(self, data):
        # Ensure document type is active
        if data.get('doc_type') and not data['doc_type'].is_active:
            raise serializers.ValidationError({
                'doc_type': 'This document type is not active'
            })
        # Ensure spa is provided
        if not data.get('spa'):
            raise serializers.ValidationError({
                'spa': 'Spa is required'
            })

        return data
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# OwnerDocument Serializers

class OwnerDocumentListSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = OwnerDocument
        fields = [
            'id', 'title', 'file', 'notes',
            'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner',
            'owner_name', 'owner_type',
            'uploaded_by', 'uploaded_by_name',
            'file_size', 'file_extension',
            'created_at', 'updated_at'
        ]
    
    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}".strip() or obj.uploaded_by.email
        return "System"
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
            except:
                return "Unknown"
        return "N/A"
    
    def get_file_extension(self, obj):
        if obj.file:
            return obj.file.name.split('.')[-1].upper()
        return "N/A"


class OwnerDocumentDetailSerializer(serializers.ModelSerializer):
    uploaded_by = UserBasicSerializer(read_only=True)
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    
    class Meta:
        model = OwnerDocument
        fields = [
            'id', 'title', 'file', 'notes',
            'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner',
            'owner_name', 'owner_type',
            'uploaded_by', 'file_size', 'file_extension',
            'created_at', 'updated_at'
        ]
    
    def get_file_size(self, obj):
        if obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
            except:
                return "Unknown"
        return "N/A"
    
    def get_file_extension(self, obj):
        if obj.file:
            return obj.file.name.split('.')[-1].upper()
        return "N/A"


class OwnerDocumentCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OwnerDocument
        fields = ['title', 'file', 'notes', 'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner']
    
    def validate(self, data):
        # Validation: Ensure only one owner is set
        owners_set = sum([
            bool(data.get('primary_owner')),
            bool(data.get('secondary_owner')),
            bool(data.get('third_owner')),
            bool(data.get('fourth_owner'))
        ])
        
        if owners_set == 0:
            raise serializers.ValidationError({
                'owner': 'At least one owner must be specified for the document'
            })
        if owners_set > 1:
            raise serializers.ValidationError({
                'owner': 'Only one owner can be specified per document'
            })
        
        return data
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
