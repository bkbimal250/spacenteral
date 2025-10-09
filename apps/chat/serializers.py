from rest_framework import serializers
from .models import ChatMessage, ChatNotification, ChatRoom
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info for chat"""
    full_name = serializers.SerializerMethodField()
    profile_picture_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'user_type', 'profile_picture', 'profile_picture_url']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email
    
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=False)
    receiver_id = serializers.IntegerField(write_only=True)
    
    # File information
    file_url = serializers.SerializerMethodField()
    file_size_human = serializers.SerializerMethodField()
    is_image = serializers.SerializerMethodField()
    is_audio = serializers.SerializerMethodField()
    is_video = serializers.SerializerMethodField()
    
    # Reply information
    reply_to_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'sender', 'receiver', 'sender_id', 'receiver_id',
            'message', 'message_type', 'file', 'file_url', 'file_name', 
            'file_size', 'file_size_human', 'file_type', 'timestamp', 
            'updated_at', 'is_read', 'read_at', 'is_delivered', 'delivered_at',
            'is_edited', 'is_deleted', 'deleted_at', 'reply_to', 'reply_to_message',
            'is_image', 'is_audio', 'is_video'
        ]
        read_only_fields = ['id', 'timestamp', 'updated_at', 'read_at', 'delivered_at', 'deleted_at']
    
    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None
    
    def get_file_size_human(self, obj):
        if obj.file_size:
            # Convert bytes to human readable format
            for unit in ['B', 'KB', 'MB', 'GB']:
                if obj.file_size < 1024.0:
                    return f"{obj.file_size:.1f} {unit}"
                obj.file_size /= 1024.0
            return f"{obj.file_size:.1f} TB"
        return None
    
    def get_is_image(self, obj):
        return obj.is_image()
    
    def get_is_audio(self, obj):
        return obj.is_audio()
    
    def get_is_video(self, obj):
        return obj.is_video()
    
    def get_reply_to_message(self, obj):
        if obj.reply_to:
            return {
                'id': obj.reply_to.id,
                'message': obj.reply_to.message,
                'sender': UserBasicSerializer(obj.reply_to.sender).data,
                'message_type': obj.reply_to.message_type,
            }
        return None
    
    def create(self, validated_data):
        # Set message type based on file presence
        if validated_data.get('file'):
            file_ext = validated_data['file'].name.split('.')[-1].lower()
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
                validated_data['message_type'] = 'image'
            elif file_ext in ['mp3', 'wav', 'ogg', 'm4a', 'aac']:
                validated_data['message_type'] = 'audio'
            elif file_ext in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']:
                validated_data['message_type'] = 'video'
            else:
                validated_data['message_type'] = 'file'
            
            # Set file information
            file_obj = validated_data['file']
            validated_data['file_name'] = file_obj.name
            validated_data['file_size'] = file_obj.size
            validated_data['file_type'] = file_obj.content_type
        
        return super().create(validated_data)


class ConversationSerializer(serializers.Serializer):
    """Serializer for conversation list with last message"""
    user = UserBasicSerializer()
    last_message = serializers.CharField(allow_null=True)
    last_message_timestamp = serializers.DateTimeField(allow_null=True)
    last_message_type = serializers.CharField(allow_null=True)
    unread_count = serializers.IntegerField()
    is_sender = serializers.BooleanField()
    is_online = serializers.BooleanField(default=False)


class ChatNotificationSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    related_message = ChatMessageSerializer(read_only=True)
    
    class Meta:
        model = ChatNotification
        fields = [
            'id', 'sender', 'notification_type', 'message', 'is_read', 
            'created_at', 'read_at', 'related_message'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    created_by = UserBasicSerializer(read_only=True)
    members = UserBasicSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'description', 'created_by', 'members', 
            'member_count', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()

