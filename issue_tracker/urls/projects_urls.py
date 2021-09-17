from django.urls import path
from issue_tracker.views.issues_views import IssueCreate
from issue_tracker.views.project_views import ProjectsList, ProjectDetail, ProjectCreate, \
    ProjectsSearch, ProjectUpdate, ProjectDelete, ProjectAddMember, ProjectDelMember


app_name = 'projects'


urlpatterns = [
    path('', ProjectsList.as_view(), name='projects_list'),
    path('<int:pk>/detail', ProjectDetail.as_view(), name='project_detail'),
    path('create', ProjectCreate.as_view(), name='project_create'),
    path('search', ProjectsSearch.as_view(), name='search'),
    path('<int:pk>/update', ProjectUpdate.as_view(), name='project_update'),
    path('<int:project_pk>/add_issue', IssueCreate.as_view(), name='issues_create'),
    path('<int:pk>/delete', ProjectDelete.as_view(), name='project_delete'),
    path('<int:project_pk>/add_member', ProjectAddMember.as_view(), name='project_add_member'),
    path('<int:project_pk>/del_member', ProjectDelMember.as_view(), name='project_del_member'),
]
