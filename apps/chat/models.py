from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recv_messages', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'chat_messages'
        indexes = [models.Index(fields=['sender', 'receiver', 'timestamp'])]
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender_id}->{self.receiver_id} @ {self.timestamp}"
