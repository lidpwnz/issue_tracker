from django.db.models import Model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from api_v1.helpers import ProjectAttrsMixin, IssueAttrsMixin
from api_v1.serializers import IssueSerializer
from issue_tracker.models import Issue


class IssueDetailsAPIView(IssueAttrsMixin, APIView):
    serializer_class: BaseSerializer = IssueSerializer
    queryset = Issue.objects.filter(is_deleted=False)

    def get_object(self) -> Issue:
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))

    def put(self, request, *args, **kwargs) -> Response:
        issue: Issue = self.get_object()
        serializer: IssueSerializer = IssueSerializer(instance=issue, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs) -> Response:
        issue: Issue = self.get_object()
        serializer: IssueSerializer = self.serializer_class(instance=issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs) -> Response:
        issue: Issue = self.get_object()
        issue.is_deleted = True
        issue.save()
        return Response({'response': 'Successfully Deleted'}, status=status.HTTP_205_RESET_CONTENT)


class IssueListAPIView(IssueAttrsMixin, APIView):
    def get(self, request, *args, **kwargs) -> Response:
        serializer: IssueSerializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs) -> Response:
        serializer: IssueSerializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProjectListAPIView(ProjectAttrsMixin, ListCreateAPIView):
    pass


class ProjectDetailsAPIView(ProjectAttrsMixin, RetrieveUpdateDestroyAPIView):
    def perform_destroy(self, instance) -> None:
        instance.is_deleted = True
        instance.save()
