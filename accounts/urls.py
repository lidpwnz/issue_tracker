from django.urls import path, include
from .views import RegisterView, MyLoginView, UserDetailView, ListUsers

app_name = 'accounts'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/profile', UserDetailView.as_view(), name='profile'),
    path('', ListUsers.as_view(), name='list_users')
]
