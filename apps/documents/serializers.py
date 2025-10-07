from rest_framework import serializers
from .models import DocumentType, Document


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'is_active']


class DocumentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    doc_type_name = serializers.CharField(source='doc_type.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'doc_type', 'doc_type_name', 'user', 'user_email', 'file',
            'notes', 'uploaded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']
