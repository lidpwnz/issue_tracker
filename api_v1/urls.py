from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import IssueDetailsAPIView, ProjectDetailsAPIView, ProjectListAPIView, IssueListAPIView

urlpatterns = [
    path('issues/<int:pk>/', IssueDetailsAPIView.as_view()),
    path('issues/', IssueListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailsAPIView.as_view()),
    path('projects/', ProjectListAPIView.as_view()),
    path('login/', obtain_auth_token)
]
