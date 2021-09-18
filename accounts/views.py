from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from issue_tracker.filters.projects_filter import ProjectFilter
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from .helpers import AccountsMixin


class MyLoginView(AccountsMixin, LoginView):
    pass


class RegisterView(AccountsMixin, CreateView):
    model = User
    template_name = 'registration/registration.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_next_url_from_request() or self.get_success_url())


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user/detail.html'
    context_object_name = 'user_obj'
    projects = None

    def get_pagination_context(self):
        paginator = Paginator(self.projects, 5)
        page = paginator.get_page(self.request.GET.get('page', 1))
        context = {'paginator': paginator, 'is_paginated': page.has_other_pages(), 'page_obj': page}

        return context

    def get_context_data(self, **kwargs):
        self.projects = list(map(lambda item: item.project, self.object.projects.all()))
        kwargs['my_filter'] = ProjectFilter(self.request.GET, queryset=self.model.objects.all())
        return super(UserDetailView, self).get_context_data(**kwargs, **self.get_pagination_context())


class ListUsers(PermissionRequiredMixin, ListView):
    template_name = 'user/list.html'
    context_object_name = 'users'
    model = User
    paginate_by = 10
    permission_required = 'auth.view_user'
