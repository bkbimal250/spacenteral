from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'short_message', 'file', 'is_read', 'timestamp']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__email', 'receiver__email', 'message']
    raw_id_fields = ['sender', 'receiver']
    ordering = ['-timestamp']

    def short_message(self, obj):
        if not obj.message:
            return ''
        return (obj.message[:60] + '…') if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message'

    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"Marked {updated} messages as read.")
    mark_as_read.short_description = 'Mark selected as read'

from django.contrib import admin

# Register your models here.
