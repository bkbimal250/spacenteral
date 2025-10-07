import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

User = get_user_model()


class DirectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        # Stable room name using sorted ids
        user_ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_group_name = f"dm_{'_'.join(user_ids)}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or '{}')
        content = data.get('message')
        file_url = data.get('file_url')
        if not content and not file_url:
            return
        msg = await self._save_message(content)
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat.message',
            'id': msg['id'],
            'sender_id': msg['sender_id'],
            'receiver_id': msg['receiver_id'],
            'message': msg['message'],
            'file_url': file_url,
            'timestamp': msg['timestamp'],
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'message': event['message'],
            'file_url': event['file_url'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def _save_message(self, content):
        receiver = User.objects.get(id=self.other_user_id)
        m = ChatMessage.objects.create(sender=self.user, receiver=receiver, message=content or None)
        return {
            'id': m.id,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
            'message': m.message,
            'timestamp': m.timestamp.isoformat(),
        }
