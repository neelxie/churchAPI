import jwt
from .models import User
from itsdangerous import URLSafeTimedSerializer
from os import environ
from django.urls import reverse

from rest_framework import authentication, exceptions

from posts.auth_token import AuthenticationToken

authentication_token = AuthenticationToken()

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        auth_headers = authentication.get_authorization_header(request).split()
        if len(auth_headers) != 2:
            return None

        token = auth_headers[1].decode("utf-8")

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        user_id = authentication_token.decode_auth_token(token)
        user = User.objects.get(pk=user_id)
        
        return (user, token)