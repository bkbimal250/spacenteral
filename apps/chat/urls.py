from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatViewSet, ChatNotificationViewSet, ChatRoomViewSet, FileDownloadView
)

router = DefaultRouter()
router.register(r'chat', ChatViewSet, basename='chat')
router.register(r'notifications', ChatNotificationViewSet, basename='notifications')
router.register(r'rooms', ChatRoomViewSet, basename='rooms')

urlpatterns = [
    path('', include(router.urls)),
    path('files/download/<int:message_id>/', FileDownloadView.as_view(), name='file-download'),
]

