# Chat Functionality Testing Guide

## Quick Backend Test

### Step 1: Start Django Server
```bash
cd C:\Users\DELL\Desktop\Bimal\spa_central
venv\Scripts\activate
python manage.py runserver
```

### Step 2: Test API Endpoints (Using Browser or Postman)

#### Get Auth Token First
You need a valid authentication token. Login via the API or get a token:

**Option A: Create a token via Django Shell**
```bash
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

# Get or create token for existing user
user = User.objects.first()  # or User.objects.get(email='your@email.com')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

**Option B: Login via Login Endpoint**
```bash
POST http://localhost:8000/api/login/
Body: { "email": "your@email.com", "password": "yourpassword" }
```

#### Test Chat Endpoints

1. **Get All Users** (to see who you can chat with)
```bash
curl -X GET http://localhost:8000/api/chat/users/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

2. **Get Conversations**
```bash
curl -X GET http://localhost:8000/api/chat/conversations/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

3. **Send a Message**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "receiver_id=2" \
  -F "message=Hello from API test!"
```

4. **Get Chat History**
```bash
curl -X GET "http://localhost:8000/api/chat/history/?user_id=2" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Frontend Testing

### Step 1: Install Dependencies
```bash
cd frontend/Dashboard/admindashbboard
npm install lucide-react
```

### Step 2: Start Frontend Dev Server
```bash
npm run dev
```

### Step 3: Test in Browser

1. **Login**: Navigate to `http://localhost:5173` and login
2. **Open Chat**: Click on "💬 Chat Messages" in the sidebar
3. **Test Features**:
   - ✅ View conversations list
   - ✅ Click "New Chat" button to see all users
   - ✅ Select a user to start chatting
   - ✅ Send a text message
   - ✅ Send a file attachment
   - ✅ Check if messages appear in real-time
   - ✅ Check unread badges
   - ✅ Search for conversations
   - ✅ Test mobile responsive view

## Expected Results

### Backend API Responses

**GET /api/chat/users/**
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

**GET /api/chat/conversations/**
```json
[
  {
    "user": {
      "id": 2,
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_type": "spa_manager"
    },
    "last_message": "Hello!",
    "last_message_timestamp": "2025-10-08T12:30:00Z",
    "unread_count": 0,
    "is_sender": true
  }
]
```

**POST /api/chat/** (Send message)
```json
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
  "message": "Hello from API test!",
  "file": null,
  "timestamp": "2025-10-08T12:35:00Z",
  "is_read": false
}
```

## Common Issues & Solutions

### Issue: "Field name `role` is not valid for model `User`"
**Status:** ✅ FIXED
**Solution:** Updated serializer to use `user_type` instead of `role`

### Issue: Cannot import 'lucide-react'
**Status:** Pending
**Solution:** Run `npm install lucide-react` in the frontend directory

### Issue: WebSocket not connecting
**Solution:** 
1. Ensure Django Channels is installed: `pip install channels`
2. Check ASGI configuration in `spa_central/asgi.py`
3. Verify WebSocket URL in frontend matches backend

### Issue: Messages not showing in real-time
**Solution:**
1. Check browser console for WebSocket errors
2. Verify WebSocket connection is established
3. Ensure both users are connected to their respective WebSocket rooms

## Database Verification

To verify messages are being stored:
```bash
python manage.py shell
```
```python
from apps.chat.models import ChatMessage

# View all messages
messages = ChatMessage.objects.all()
for msg in messages:
    print(f"{msg.sender.email} -> {msg.receiver.email}: {msg.message}")

# Count messages
print(f"Total messages: {ChatMessage.objects.count()}")

# Get messages between two users
from django.contrib.auth import get_user_model
User = get_user_model()
user1 = User.objects.get(id=1)
user2 = User.objects.get(id=2)

conversation = ChatMessage.objects.filter(
    sender__in=[user1, user2],
    receiver__in=[user1, user2]
).order_by('timestamp')

for msg in conversation:
    print(f"{msg.sender.email}: {msg.message} ({msg.timestamp})")
```

## Performance Check

Test with multiple users and messages:
```python
# In Django shell
from apps.chat.models import ChatMessage
from django.contrib.auth import get_user_model
import random

User = get_user_model()
users = list(User.objects.all())

# Create test messages
for i in range(50):
    sender = random.choice(users)
    receiver = random.choice([u for u in users if u != sender])
    ChatMessage.objects.create(
        sender=sender,
        receiver=receiver,
        message=f"Test message {i}"
    )

print(f"Created {ChatMessage.objects.count()} messages")
```

## Next Steps After Testing

Once testing is complete:
1. ✅ Verify all API endpoints work
2. ✅ Confirm real-time messaging works
3. ✅ Test file uploads
4. ✅ Test on mobile view
5. Consider adding:
   - Message notifications
   - Typing indicators
   - Online status
   - Message reactions
   - Group chats

## Support

If you encounter any issues:
1. Check Django server logs for backend errors
2. Check browser console for frontend errors
3. Verify all dependencies are installed
4. Ensure database migrations are applied
5. Confirm authentication tokens are valid

