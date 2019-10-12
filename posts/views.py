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

from .renderers import UserJSONRenderer
from .serializers import UserSerializer

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