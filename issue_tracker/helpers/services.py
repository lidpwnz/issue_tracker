from abc import abstractmethod

from issue_tracker.models import Project, Issue
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View


def get_all_projects():
    return Project.objects.filter(is_deleted=False)


def get_issues():
    return Issue.objects.filter(is_deleted=False)


class IsUserInObjectListMixin(UserPassesTestMixin, SingleObjectMixin, View):

    @abstractmethod
    def get_object_list(self):
        raise NotImplementedError

    def test_func(self):
        object_list = self.get_object_list()
        return self.request.user in object_list or self.request.user.is_superuser


class ProjectUserPassesTestMixin(IsUserInObjectListMixin):
    object = None

    def get_object_list(self):
        return self.get_object().users.all()

