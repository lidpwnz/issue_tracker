from django.db.models import QuerySet

from api_v1.serializers import ProjectSerializer, IssueSerializer
from issue_tracker.models import Project, Issue


class ProjectAttrsMixin:
    queryset: QuerySet = Project.objects.filter(is_deleted=False)
    serializer_class: ProjectSerializer = ProjectSerializer


class IssueAttrsMixin:
    serializer_class = IssueSerializer
    queryset: QuerySet = Issue.objects.filter(is_deleted=False)
