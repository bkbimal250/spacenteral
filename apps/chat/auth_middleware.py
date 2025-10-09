from urllib.parse import parse_qs
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async

User = get_user_model()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Get the token from query parameters
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get('token', [None])[0]

        user = None
        if token_key:
            try:
                token = await self.get_token(token_key)
                if token:
                    user = await self.get_user(token.user_id)
            except Exception as e:
                print(f"Auth error: {e}")
                pass

        scope['user'] = user
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_token(self, token_key):
        """Get token from database"""
        try:
            return Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        """Get user from database"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
