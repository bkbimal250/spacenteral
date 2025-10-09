from django.db import models
from django.conf import settings
import os


class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text Message'),
        ('file', 'File Attachment'),
        ('image', 'Image'),
        ('audio', 'Audio Message'),
        ('video', 'Video Message'),
        ('system', 'System Message'),
    )
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recv_messages', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    
    # File handling
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Message editing/deletion
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Reply functionality
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        db_table = 'chat_messages'
        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender_id}->{self.receiver_id} @ {self.timestamp}"
    
    def get_file_extension(self):
        if self.file and self.file.name:
            return os.path.splitext(self.file.name)[1].lower()
        return None
    
    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.get_file_extension() in image_extensions
    
    def is_audio(self):
        audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
        return self.get_file_extension() in audio_extensions
    
    def is_video(self):
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
        return self.get_file_extension() in video_extensions


class ChatNotification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'New Message'),
        ('file', 'File Shared'),
        ('typing', 'User Typing'),
        ('online', 'User Online'),
        ('offline', 'User Offline'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Related message (if applicable)
    related_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        db_table = 'chat_notifications'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.user.email}"


class ChatRoom(models.Model):
    """Group chat rooms (future implementation)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_rooms', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_rooms'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
