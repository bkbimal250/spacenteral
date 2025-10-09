import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import ChatMessage, ChatNotification

User = get_user_model()


class DirectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user from token
        user = self.scope.get('user')
        
        if not user or user.is_anonymous:
            await self.close()
            return
        
        self.user = user
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Validate that user can chat with this other user
        try:
            other_user = await self.get_user(self.other_user_id)
            if not other_user:
                await self.close()
                return
        except:
            await self.close()
            return
        
        # Stable room name using sorted ids
        user_ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_group_name = f"dm_{'_'.join(user_ids)}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        print(f"WebSocket connected: {self.user.email} -> {other_user.email}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or '{}')
        message_type = data.get('type', 'message')
        
        if message_type == 'message':
            await self._handle_message(data)
        elif message_type == 'typing':
            await self._handle_typing(data)
        elif message_type == 'read_receipt':
            await self._handle_read_receipt(data)
    
    async def _handle_message(self, data):
        content = data.get('message')
        file_url = data.get('file_url')
        message_type = data.get('message_type', 'text')
        reply_to_id = data.get('reply_to_id')
        
        if not content and not file_url:
            return
            
        msg = await self._save_message(content, message_type, file_url, reply_to_id)
        
        # Send message to room
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat.message',
            'id': msg['id'],
            'sender_id': msg['sender_id'],
            'receiver_id': msg['receiver_id'],
            'message': msg['message'],
            'message_type': msg['message_type'],
            'file_url': msg.get('file_url'),
            'file_name': msg.get('file_name'),
            'file_size': msg.get('file_size'),
            'file_type': msg.get('file_type'),
            'timestamp': msg['timestamp'],
            'reply_to': msg.get('reply_to'),
        })
        
        # Create notification for receiver
        await self._create_notification(msg)
    
    async def _handle_typing(self, data):
        is_typing = data.get('is_typing', False)
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'typing.indicator',
            'user_id': self.user.id,
            'is_typing': is_typing,
        })
    
    async def _handle_read_receipt(self, data):
        message_ids = data.get('message_ids', [])
        if message_ids:
            await self._mark_messages_read(message_ids)
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'read.receipt',
                'user_id': self.user.id,
                'message_ids': message_ids,
            })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'id': event['id'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'message': event['message'],
            'message_type': event['message_type'],
            'file_url': event.get('file_url'),
            'file_name': event.get('file_name'),
            'file_size': event.get('file_size'),
            'file_type': event.get('file_type'),
            'timestamp': event['timestamp'],
            'reply_to': event.get('reply_to'),
        }))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'is_typing': event['is_typing'],
        }))
    
    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'user_id': event['user_id'],
            'message_ids': event['message_ids'],
        }))

    @database_sync_to_async
    def _save_message(self, content, message_type='text', file_url=None, reply_to_id=None):
        receiver = User.objects.get(id=self.other_user_id)
        
        # Get reply message if provided
        reply_to = None
        if reply_to_id:
            try:
                reply_to = ChatMessage.objects.get(id=reply_to_id)
            except ChatMessage.DoesNotExist:
                pass
        
        m = ChatMessage.objects.create(
            sender=self.user, 
            receiver=receiver, 
            message=content or None,
            message_type=message_type,
            reply_to=reply_to
        )
        
        return {
            'id': m.id,
            'sender_id': m.sender_id,
            'receiver_id': m.receiver_id,
            'message': m.message,
            'message_type': m.message_type,
            'file_url': file_url,
            'file_name': m.file_name,
            'file_size': m.file_size,
            'file_type': m.file_type,
            'timestamp': m.timestamp.isoformat(),
            'reply_to': reply_to.id if reply_to else None,
        }
    
    @database_sync_to_async
    def _create_notification(self, msg):
        """Create notification for the receiver"""
        receiver = User.objects.get(id=msg['receiver_id'])
        
        notification_message = f"New message from {self.user.first_name or self.user.email}"
        if msg['message_type'] == 'file':
            notification_message = f"File shared by {self.user.first_name or self.user.email}"
        elif msg['message_type'] == 'image':
            notification_message = f"Image shared by {self.user.first_name or self.user.email}"
        
        ChatNotification.objects.create(
            user=receiver,
            sender=self.user,
            notification_type='message',
            message=notification_message,
            related_message_id=msg['id']
        )
    
    @database_sync_to_async
    def _mark_messages_read(self, message_ids):
        """Mark messages as read"""
        ChatMessage.objects.filter(
            id__in=message_ids,
            receiver=self.user
        ).update(is_read=True, read_at=timezone.now())
    
    @database_sync_to_async
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
