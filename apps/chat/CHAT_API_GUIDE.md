# Chat API Guide

## Overview
This guide describes the Chat API endpoints for the SpaCentral Admin Dashboard. The chat system supports real-time messaging using WebSockets and REST API for message history and management.

## Features
- ✅ Real-time messaging with WebSocket
- ✅ Message history and persistence
- ✅ Unread message counts
- ✅ File attachments support
- ✅ Read receipts
- ✅ Conversation management
- ✅ User search for new chats

## Database Schema

### ChatMessage Model
```python
- sender: ForeignKey to User
- receiver: ForeignKey to User
- message: TextField (nullable)
- file: FileField (nullable, uploads to 'chat_files/%Y/%m/%d/')
- timestamp: DateTimeField (auto)
- is_read: BooleanField (default: False)
```

## REST API Endpoints

### Authentication
All endpoints require authentication via Token in the Authorization header:
```
Authorization: Token <your-token-here>
```

### 1. Get All Conversations
**Endpoint:** `GET /api/chat/conversations/`

**Description:** Get list of all conversations with last message and unread count.

**Response:**
```json
[
  {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_type": "spa_manager"
    },
    "last_message": "Hello, how are you?",
    "last_message_timestamp": "2025-10-08T10:30:00Z",
    "unread_count": 3,
    "is_sender": true
  }
]
```

### 2. Get Chat History
**Endpoint:** `GET /api/chat/history/?user_id={user_id}`

**Description:** Get complete chat history with a specific user. Automatically marks unread messages as read.

**Query Parameters:**
- `user_id` (required): The ID of the other user

**Response:**
```json
[
  {
    "id": 1,
    "sender": {
      "id": 1,
      "email": "admin@example.com",
      "full_name": "Admin User",
      "user_type": "admin"
    },
    "receiver": {
      "id": 2,
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_type": "spa_manager"
    },
    "message": "Hello, how can I help you?",
    "file": null,
    "timestamp": "2025-10-08T10:30:00Z",
    "is_read": true
  }
]
```

### 3. Send Message
**Endpoint:** `POST /api/chat/`

**Description:** Send a new message to a user.

**Request Body (multipart/form-data):**
```json
{
  "receiver_id": 2,
  "message": "Hello there!",
  "file": <file object> (optional)
}
```

**Response:**
```json
{
  "id": 10,
  "sender": {
    "id": 1,
    "email": "admin@example.com",
    "full_name": "Admin User",
    "user_type": "admin"
  },
  "receiver": {
    "id": 2,
    "email": "user@example.com",
    "full_name": "John Doe",
    "user_type": "spa_manager"
  },
  "message": "Hello there!",
  "file": null,
  "timestamp": "2025-10-08T10:35:00Z",
  "is_read": false
}
```

### 4. Get All Users
**Endpoint:** `GET /api/chat/users/`

**Description:** Get list of all users (excluding current user) for starting new conversations.

**Response:**
```json
[
  {
    "id": 2,
    "email": "user@example.com",
    "full_name": "John Doe",
    "user_type": "spa_manager"
  }
]
```

### 5. Mark Messages as Read
**Endpoint:** `POST /api/chat/mark_read/`

**Description:** Mark all messages from a specific user as read.

**Request Body:**
```json
{
  "user_id": 2
}
```

**Response:**
```json
{
  "success": true
}
```

## WebSocket Connection

### Connection URL
```
ws://localhost:8000/ws/chat/{user_id}/
wss://your-domain.com/ws/chat/{user_id}/
```

Where `{user_id}` is the ID of the user you want to chat with.

### Authentication
WebSocket authentication is handled via Django Channels middleware. Ensure user is authenticated before connecting.

### Sending Messages
```javascript
ws.send(JSON.stringify({
  message: "Hello!",
  file_url: null
}));
```

### Receiving Messages
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  /*
  {
    id: 10,
    sender_id: 1,
    receiver_id: 2,
    message: "Hello!",
    file_url: null,
    timestamp: "2025-10-08T10:35:00Z"
  }
  */
};
```

## Frontend Integration

### File Structure
```
frontend/Dashboard/admindashbboard/src/
├── pages/
│   └── Chat.jsx                    # Main chat page
├── components/Files/Chats/
│   ├── ChatList.jsx               # Conversation list
│   ├── ChatWindow.jsx             # Main chat window
│   ├── MessageBubble.jsx          # Individual message
│   ├── ChatInput.jsx              # Message input component
│   └── NewChatModal.jsx           # Modal for starting new chat
└── services/
    └── chatService.js             # API service functions
```

### Using the Chat Service
```javascript
import chatService from '../services/chatService';

// Get conversations
const conversations = await chatService.getConversations();

// Get chat history
const messages = await chatService.getChatHistory(userId);

// Send message
await chatService.sendMessage(receiverId, message, file);

// Mark as read
await chatService.markAsRead(userId);

// Get WebSocket URL
const wsUrl = chatService.getWebSocketUrl(userId);
```

### Features in UI
- **Messenger-style layout**: Split view with conversation list and chat window
- **Real-time updates**: WebSocket integration for instant messaging
- **Responsive design**: Mobile-friendly with adaptive layout
- **Search functionality**: Filter conversations
- **Unread indicators**: Badge showing unread message count
- **Read receipts**: Double check marks for read messages
- **File attachments**: Support for uploading and sharing files
- **User avatars**: Color-coded initials as avatars
- **Timestamps**: Smart time formatting (time, day, or date)

## Testing the API

### Using cURL

1. **Get Conversations:**
```bash
curl -X GET http://localhost:8000/api/chat/conversations/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

2. **Send Message:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "receiver_id=2" \
  -F "message=Hello from API!"
```

3. **Get Chat History:**
```bash
curl -X GET "http://localhost:8000/api/chat/history/?user_id=2" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Using Postman

1. Create a new request
2. Set Authorization header: `Token YOUR_TOKEN_HERE`
3. Test endpoints as described above

## Common Issues & Solutions

### Issue: WebSocket not connecting
**Solution:** Ensure Django Channels and Daphne are properly configured in settings.py and ASGI is set up.

### Issue: Messages not showing in real-time
**Solution:** Check that WebSocket connection is active and event handlers are properly set up.

### Issue: File uploads not working
**Solution:** Ensure MEDIA_URL and MEDIA_ROOT are configured in settings.py and media serving is enabled.

### Issue: 401 Unauthorized errors
**Solution:** Verify authentication token is valid and included in request headers.

## Environment Variables

Add to your `.env` file:
```env
# Backend
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_HOST=localhost:8000
```

## Security Considerations

- ✅ All endpoints require authentication
- ✅ Users can only view their own conversations
- ✅ File uploads are validated and stored securely
- ✅ WebSocket connections are authenticated
- ✅ SQL injection protection via Django ORM
- ✅ XSS protection in frontend components

## Performance Tips

1. **Pagination**: For large chat histories, implement pagination
2. **Caching**: Cache conversation lists to reduce database queries
3. **Lazy Loading**: Load messages on demand as user scrolls
4. **Connection Management**: Properly close WebSocket connections when not in use
5. **File Compression**: Compress file attachments before upload

## Next Steps

- [ ] Add typing indicators
- [ ] Add message editing/deletion
- [ ] Add group chat support
- [ ] Add voice/video call integration
- [ ] Add emoji picker
- [ ] Add message search functionality
- [ ] Add notification system

