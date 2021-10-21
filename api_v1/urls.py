from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import UpdateAPIView

urlpatterns = [
    path('issues/<int:pk>/', UpdateAPIView.as_view()),
    path('login/', obtain_auth_token)
]
