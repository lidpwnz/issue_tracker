from django.urls import path, include
from .views import RegisterView, MyLoginView, UserDetailView, ListUsers, UserUpdateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'acc'

urlpatterns = [

    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/profile', UserDetailView.as_view(), name='profile'),
    path('', ListUsers.as_view(), name='list_users'),
    path('<int:pk>/update', UserUpdateView.as_view(), name='user_update'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy('acc:password_reset_done')),
         name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('acc:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
