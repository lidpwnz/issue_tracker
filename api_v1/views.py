from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView

from api_v1.serializers import IssueSerializer
from issue_tracker.models import Issue


class DetailsAPIView(APIView):
    serializer_class: BaseSerializer = IssueSerializer
    queryset = Issue.objects.all()

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))

    def put(self, request, *args, **kwargs) -> Response:
        issue: Issue = self.get_object()
        serializer: IssueSerializer = IssueSerializer(instance=issue, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        issue: Issue = self.get_object()
        serializer: IssueSerializer = IssueSerializer(instance=issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response({'response': 'Successfully Deleted'}, status=status.HTTP_205_RESET_CONTENT)

