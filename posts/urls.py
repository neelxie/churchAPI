from django.urls import path
from .views import UserRetrieveUpdateAPIView

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
]
