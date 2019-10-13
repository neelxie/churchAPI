from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import User

from itsdangerous import URLSafeTimedSerializer, exc
from django.core.mail import send_mail

import os, re

from google.auth.transport import requests
from google.oauth2 import id_token

from .renderers import UserJSONRenderer
from .serializers import UserSerializer, GoogleSerializer
from .validate import ValidateUser


check_user = ValidateUser()

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    """
    retrieve: Get User Details
    Update: Update User Details
    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class GoogleAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = GoogleSerializer

    def post(self, request):

        user_data = request.data.get("user", {})
        googl_auth_token = user_data.get("access_token")
        # get the token
        try:
            user_cred = id_token.verify_oauth2_token(
                googl_auth_token, requests.Request())

            verified_user = check_user.validate_system_user(user_cred)

            return Response(verified_user, status=status.HTTP_200_OK)
            
        except:
            return Response(
                {"error": "google login failed. Token is either invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
