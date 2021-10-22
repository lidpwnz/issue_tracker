from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from issue_tracker.models import Issue, Type, Project, Status


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'title']


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'title']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(ModelSerializer):
    users: ModelSerializer = UserSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'is_deleted', 'users', 'create_date', 'end_date']
        read_only = ['id', 'is_deleted']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'summary', 'description', 'status', 'type', 'project', 'is_deleted', 'created_at', 'updated_at']
        read_only = ['id', 'created_at', 'updated_at', 'is_deleted']

