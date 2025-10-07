# API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

### Obtain Token
```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Using Token
Include the token in the Authorization header:
```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## User Management

### Register User
```http
POST /api/users/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "customer",
    "phone": "+1234567890"
}
```

### Get Current User Profile
```http
GET /api/users/me/
Authorization: Token {your_token}
```

### Update Current User
```http
PATCH /api/users/me/
Authorization: Token {your_token}
Content-Type: application/json

{
    "first_name": "Jane",
    "phone": "+9876543210"
}
```

### Change Password
```http
POST /api/users/change_password/
Authorization: Token {your_token}
Content-Type: application/json

{
    "old_password": "oldpass123",
    "new_password": "newpass123",
    "new_password2": "newpass123"
}
```

## Location Management

### List Countries
```http
GET /api/countries/
```

**Query Parameters:**
- `search`: Search by name or code

### List States
```http
GET /api/states/
```

**Query Parameters:**
- `country`: Filter by country ID
- `search`: Search by name or code

### List Cities
```http
GET /api/cities/
```

**Query Parameters:**
- `state`: Filter by state ID
- `state__country`: Filter by country ID
- `search`: Search by name

### List Areas
```http
GET /api/areas/
```

**Query Parameters:**
- `city`: Filter by city ID
- `search`: Search by name or postal code

## Spa Management

### List Spas
```http
GET /api/spas/
```

**Query Parameters:**
- `search`: Search in name, description, area, city
- `status`: Filter by status (active, inactive, pending, rejected)
- `is_featured`: Filter featured spas (true/false)
- `min_rating`: Minimum rating filter
- `max_rating`: Maximum rating filter
- `city`: Filter by city ID
- `city_name`: Filter by city name (partial match)
- `state`: Filter by state ID
- `country`: Filter by country ID
- `ordering`: Sort results (rating, created_at, name, -rating, etc.)

**Example:**
```http
GET /api/spas/?city_name=New%20York&min_rating=4&is_featured=true
```

### Get Spa Details
```http
GET /api/spas/{slug}/
```

### Create Spa
```http
POST /api/spas/
Authorization: Token {your_token}
Content-Type: multipart/form-data

{
    "name": "Luxury Spa",
    "description": "A premium spa experience",
    "area": 1,
    "address": "123 Spa Street",
    "phone": "+1234567890",
    "email": "info@luxuryspa.com",
    "logo": <file>,
    "cover_image": <file>
}
```

### Get Featured Spas
```http
GET /api/spas/featured/
```

### Get Spa Services
```http
GET /api/spas/{slug}/services/
```

### Get Spa Reviews
```http
GET /api/spas/{slug}/reviews/
```

## Service Management

### List Services
```http
GET /api/services/
```

**Query Parameters:**
- `spa`: Filter by spa ID
- `is_active`: Filter active services
- `search`: Search in name or description

### Create Service
```http
POST /api/services/
Authorization: Token {your_token}
Content-Type: application/json

{
    "spa": 1,
    "name": "Swedish Massage",
    "description": "Relaxing full body massage",
    "duration": 60,
    "price": "99.99",
    "discounted_price": "79.99",
    "is_active": true
}
```

## Review Management

### List Reviews
```http
GET /api/reviews/
```

**Query Parameters:**
- `spa`: Filter by spa ID
- `rating`: Filter by rating (1-5)

### Create Review
```http
POST /api/reviews/
Authorization: Token {your_token}
Content-Type: application/json

{
    "spa": 1,
    "rating": 5,
    "title": "Amazing experience!",
    "comment": "The spa was incredible. Highly recommend!"
}
```

### Get My Reviews
```http
GET /api/reviews/my_reviews/
Authorization: Token {your_token}
```

## Booking Management

### List Bookings
```http
GET /api/bookings/
Authorization: Token {your_token}
```

**Query Parameters:**
- `status`: Filter by status (pending, confirmed, cancelled, completed, no_show)
- `payment_status`: Filter by payment status
- `booking_date`: Filter by booking date (YYYY-MM-DD)

### Create Booking
```http
POST /api/bookings/
Authorization: Token {your_token}
Content-Type: application/json

{
    "spa": 1,
    "service": 1,
    "booking_date": "2024-12-25",
    "booking_time": "14:00:00",
    "notes": "First time customer"
}
```

### Cancel Booking
```http
POST /api/bookings/{id}/cancel/
Authorization: Token {your_token}
Content-Type: application/json

{
    "reason": "Change of plans"
}
```

### Confirm Booking (Spa Owner)
```http
POST /api/bookings/{id}/confirm/
Authorization: Token {your_token}
```

## Favorites

### List Favorites
```http
GET /api/favorites/
Authorization: Token {your_token}
```

### Add to Favorites
```http
POST /api/favorites/
Authorization: Token {your_token}
Content-Type: application/json

{
    "spa": 1
}
```

### Toggle Favorite
```http
POST /api/favorites/toggle/
Authorization: Token {your_token}
Content-Type: application/json

{
    "spa": 1
}
```

**Response:**
```json
{
    "status": "added"  // or "removed"
}
```

## Document Management

### List Documents
```http
GET /api/documents/
Authorization: Token {your_token}
```

**Query Parameters:**
- `spa`: Filter by spa ID
- `status`: Filter by status (pending, verified, rejected, expired)
- `document_type`: Filter by type (license, certificate, insurance, etc.)

### Upload Document
```http
POST /api/documents/
Authorization: Token {your_token}
Content-Type: multipart/form-data

{
    "spa": 1,
    "document_type": "license",
    "title": "Business License",
    "description": "Valid until 2025",
    "file": <file>,
    "issue_date": "2024-01-01",
    "expiry_date": "2025-12-31"
}
```

### Verify Document (Admin Only)
```http
POST /api/documents/{id}/verify/
Authorization: Token {admin_token}
```

### Reject Document (Admin Only)
```http
POST /api/documents/{id}/reject/
Authorization: Token {admin_token}
Content-Type: application/json

{
    "reason": "Document is not clear"
}
```

## WebSocket Endpoints

### Chat Room Connection
```
ws://localhost:8000/ws/chat/{room_id}/
```

**Send Message:**
```json
{
    "type": "chat_message",
    "message": "Hello!",
    "message_type": "text"
}
```

**Typing Indicator:**
```json
{
    "type": "typing",
    "is_typing": true
}
```

**Read Receipt:**
```json
{
    "type": "read_receipt",
    "message_id": 123
}
```

### Notifications Connection
```
ws://localhost:8000/ws/notifications/
```

## Pagination

All list endpoints support pagination:

**Request:**
```http
GET /api/spas/?page=2&page_size=20
```

**Response:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/spas/?page=3",
    "previous": "http://localhost:8000/api/spas/?page=1",
    "results": [...]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting

API rate limits (if configured):
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

## Best Practices

1. Always use HTTPS in production
2. Store tokens securely
3. Include proper error handling
4. Use pagination for large datasets
5. Implement proper timeout handling
6. Cache responses when appropriate

## Support

For API issues or questions:
- GitHub Issues: [Project Repository]
- Email: support@spacentral.com
- Documentation: [Full Documentation Link]

