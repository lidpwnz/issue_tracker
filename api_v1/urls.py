from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import DetailsAPIView

urlpatterns = [
    path('issues/<int:pk>/', DetailsAPIView.as_view()),
    path('login/', obtain_auth_token)
]
