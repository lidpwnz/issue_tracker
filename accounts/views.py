from django.conf import settings
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from issue_tracker.filters.projects_filter import ProjectFilter
from .forms import CreateUserForm, ProfileUpdateForm, UserUpdateForm, UserChangePasswordForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .helpers import AccountsMixin
from django.urls import reverse_lazy
from accounts.helpers import DeleteOldPhotoMixin


class MyLoginView(AccountsMixin, auth_views.LoginView):
    pass


class RegisterView(AccountsMixin, CreateView):
    model = User
    template_name = 'registration/registration.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user/detail.html'
    context_object_name = 'user_obj'
    projects = None

    def get_pagination_context(self):
        paginator = Paginator(self.get_projects(), 5)
        page = paginator.get_page(self.request.GET.get('page', 1))
        context = {'paginator': paginator, 'is_paginated': page.has_other_pages(), 'page_obj': page}

        return context

    def get_projects(self):
        return self.object.projects.all()

    def get_context_data(self, **kwargs):
        kwargs['my_filter'] = ProjectFilter(self.request.GET, queryset=self.model.objects.all())
        return super(UserDetailView, self).get_context_data(**kwargs, **self.get_pagination_context())


class ListUsers(PermissionRequiredMixin, ListView):
    template_name = 'user/list.html'
    context_object_name = 'users'
    model = User
    paginate_by = 10
    permission_required = 'auth.view_user'


class UserUpdateView(UserPassesTestMixin, DeleteOldPhotoMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/update.html'
    form_class = UserUpdateForm
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.my_form_valid_method(form, profile_form)
        else:
            return self.my_form_invalid_method(form, profile_form)

    def my_form_valid_method(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def my_form_invalid_method(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
            self.delete_old_photo()

        return ProfileUpdateForm(**form_kwargs)

    def get_success_url(self):
        return reverse_lazy('acc:profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user == self.get_object()


class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/change_password.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('acc:profile', kwargs={'pk': self.object.pk})


class UserDeletePhotoView(DeleteOldPhotoMixin, DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        avatar = self.request.POST.get('avatar')
        self.delete_old_photo(avatar=avatar)

        self.object.profile.avatar = settings.AVATARS_DEFAULT_VALUE
        self.object.profile.save()
        return redirect('acc:profile', pk=self.object.pk)
