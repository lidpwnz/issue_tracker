from django.urls import path
from issue_tracker.views.issues_views import IssuesList, IssueEdit, IssueDelete, IssueDetail

app_name = 'issues'

urlpatterns = [
    path('', IssuesList.as_view(), name='issues_list'),
    path('<int:pk>/update', IssueEdit.as_view(), name='issues_update'),
    path('<int:pk>/delete', IssueDelete.as_view(), name='issues_delete'),
    path('<int:pk>/detail', IssueDetail.as_view(), name='issues_detail')
]
