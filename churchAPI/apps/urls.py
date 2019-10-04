from django.urls import path
from .views import (
    UserRetrieveUpdateAPIView, GoogleAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('auth/google/', GoogleAPIView.as_view(), name="auth-google"),
 ]

