from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q, Max, Count, Case, When, Value, IntegerField, OuterRef, Subquery
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import ChatMessage, ChatNotification, ChatRoom
from .serializers import (
    ChatMessageSerializer, UserBasicSerializer, ConversationSerializer,
    ChatNotificationSerializer, ChatRoomSerializer
)

User = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    """ViewSet for chat messages"""
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get messages for current user"""
        user = self.request.user
        return ChatMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('timestamp')
    
    def create(self, request, *args, **kwargs):
        """Send a new message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Get list of all conversations with last message"""
        user = request.user
        
        # Get all users the current user has chatted with
        sent_to = ChatMessage.objects.filter(sender=user).values_list('receiver_id', flat=True).distinct()
        received_from = ChatMessage.objects.filter(receiver=user).values_list('sender_id', flat=True).distinct()
        user_ids = set(sent_to) | set(received_from)
        
        conversations = []
        for other_user_id in user_ids:
            other_user = User.objects.get(id=other_user_id)
            
            # Get last message in conversation
            last_msg = ChatMessage.objects.filter(
                Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
            ).order_by('-timestamp').first()
            
            # Count unread messages from other user
            unread_count = ChatMessage.objects.filter(
                sender=other_user, receiver=user, is_read=False
            ).count()
            
            conversations.append({
                'user': other_user,
                'last_message': last_msg.message if last_msg else None,
                'last_message_timestamp': last_msg.timestamp if last_msg else None,
                'unread_count': unread_count,
                'is_sender': last_msg.sender == user if last_msg else False
            })
        
        # Sort by last message timestamp
        conversations.sort(key=lambda x: x['last_message_timestamp'] or '', reverse=True)
        
        # Add message type and online status
        for conv in conversations:
            if conv['last_message_timestamp']:
                last_msg = ChatMessage.objects.filter(
                    Q(sender=user, receiver=conv['user']) | Q(sender=conv['user'], receiver=user)
                ).order_by('-timestamp').first()
                conv['last_message_type'] = last_msg.message_type if last_msg else None
            conv['is_online'] = False  # TODO: Implement online status
        
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get chat history with a specific user"""
        other_user_id = request.query_params.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get messages between current user and other user
        messages = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=other_user) | 
            Q(sender=other_user, receiver=request.user)
        ).select_related('sender', 'receiver').order_by('timestamp')
        
        # Mark messages as read
        ChatMessage.objects.filter(
            sender=other_user, receiver=request.user, is_read=False
        ).update(is_read=True)
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get list of all users (for starting new conversations)"""
        users = User.objects.exclude(id=request.user.id).order_by('email')
        serializer = UserBasicSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """Mark messages as read"""
        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        ChatMessage.objects.filter(
            sender_id=other_user_id, receiver=request.user, is_read=False
        ).update(is_read=True)
        
        return Response({'success': True})
    
    @action(detail=True, methods=['patch'])
    def edit_message(self, request, pk=None):
        """Edit a message"""
        message = self.get_object()
        
        # Only sender can edit their own messages
        if message.sender != request.user:
            return Response({'error': 'You can only edit your own messages'}, status=status.HTTP_403_FORBIDDEN)
        
        # Only allow editing text messages
        if message.message_type != 'text':
            return Response({'error': 'Only text messages can be edited'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_message = request.data.get('message')
        if not new_message:
            return Response({'error': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        message.message = new_message
        message.is_edited = True
        message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_message(self, request, pk=None):
        """Delete a message (soft delete)"""
        message = self.get_object()
        
        # Only sender can delete their own messages
        if message.sender != request.user:
            return Response({'error': 'You can only delete your own messages'}, status=status.HTTP_403_FORBIDDEN)
        
        message.is_deleted = True
        message.deleted_at = timezone.now()
        message.save()
        
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get total unread message count"""
        count = ChatMessage.objects.filter(
            receiver=request.user, is_read=False, is_deleted=False
        ).count()
        return Response({'unread_count': count})


class ChatNotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for chat notifications"""
    serializer_class = ChatNotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatNotification.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        ChatNotification.objects.filter(
            user=request.user, is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count"""
        count = ChatNotification.objects.filter(
            user=request.user, is_read=False
        ).count()
        return Response({'unread_count': count})


class FileDownloadView(APIView):
    """Handle file downloads from chat"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, message_id):
        try:
            message = ChatMessage.objects.get(id=message_id)
            
            # Check if user has access to this message
            if message.sender != request.user and message.receiver != request.user:
                return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            
            if not message.file:
                return Response({'error': 'No file attached'}, status=status.HTTP_404_NOT_FOUND)
            
            # Serve the file
            file_path = message.file.path
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type=message.file_type or 'application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{message.file_name or os.path.basename(file_path)}"'
                    return response
            else:
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
                
        except ChatMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)


class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for group chat rooms (future implementation)"""
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatRoom.objects.filter(members=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        room = serializer.save(created_by=self.request.user)
        room.members.add(self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add member to chat room"""
        room = self.get_object()
        
        # Only room creator can add members
        if room.created_by != request.user:
            return Response({'error': 'Only room creator can add members'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            room.members.add(user)
            return Response({'status': 'success'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove member from chat room"""
        room = self.get_object()
        
        # Only room creator can remove members
        if room.created_by != request.user:
            return Response({'error': 'Only room creator can remove members'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            room.members.remove(user)
            return Response({'status': 'success'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
