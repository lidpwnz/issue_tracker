from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from issue_tracker.filters.issues_filter import IssueFilter
from issue_tracker.forms.project_form import ProjectForm
from issue_tracker.helpers.views import SearchView, MembersOperationsMixin
from issue_tracker.models import Project
from issue_tracker.filters.projects_filter import ProjectFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from issue_tracker.helpers.services import ProjectUserPassesTestMixin


class ProjectsList(ListView):
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    model = Project
    ordering = ['end_date', '-create_date']
    filter_object = None
    paginate_by = 5
    extra_context = {'btn_text': 'Filter'}

    def get(self, request, *args, **kwargs):
        self.filter_object = self.get_filter_object()
        return super(ProjectsList, self).get(request, *args, **kwargs)

    def get_filter_object(self):
        return ProjectFilter(self.request.GET, queryset=self.model.objects.filter(is_deleted=False))

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(my_filter=self.filter_object)

    def get_queryset(self):
        return self.filter_object.qs


class ProjectDetail(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("There is no such project!")
        else:
            return super(ProjectDetail, self).get(request, *args, **kwargs)

    def get_paginator(self):
        return Paginator(self.get_filter().qs, 5)

    def get_pagination_context(self):
        paginator = self.get_paginator()
        page = paginator.get_page(self.request.GET.get('page', 1))

        context = {
            'is_paginated': page.has_other_pages(),
            'issues': page.object_list,
            'page_obj': page,
            'paginator': paginator
        }

        return context

    def get_issues(self):
        return self.object.issues.filter(is_deleted=False).order_by('-created_at')

    def get_filter(self):
        return IssueFilter(self.request.GET, queryset=self.get_issues())

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        project_users = self.object.users.values_list('id', flat=True)
        users_not_in_project = get_user_model().objects.exclude(id__in=project_users)
        context.update({'my_filter': self.get_filter(), 'btn_text': 'Filter', **self.get_pagination_context(),
                        'users_not_in_project': users_not_in_project, 'project_users': project_users})
        return context


class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project.html'
    extra_context = {'btn_text': 'Create Project', 'url': reverse_lazy('projects:project_create')}
    success_url = reverse_lazy('projects:projects_list')
    object = None
    permission_required = 'issue_tracker.add_project'

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return redirect(self.get_success_url())


class ProjectUpdate(ProjectUserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project.html'
    extra_context = {'btn_text': 'Update Project'}
    permission_required = 'issue_tracker.change_project'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['create_date'].widget.attrs.update({'min': self.object.create_date})
        form.fields['end_date'].widget.attrs.update({'min': self.object.create_date})
        return form

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        context['url'] = reverse('projects:project_update', kwargs={'pk': self.object.pk})
        return context

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.pk})


class ProjectsSearch(SearchView):
    search_fields = ['title', '|description', '|issues__summary']
    search_fields_methods = ['icontains', 'icontains', 'icontains']


class ProjectDelete(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects:projects_list')
    permission_required = 'issue_tracker.delete_project'

    def test_func(self):
        return self.request.user in self.get_object().users.all()

    def delete(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.save()
        return redirect(self.success_url)


class ProjectAddMember(MembersOperationsMixin):
    def action(self):
        user = self.get_user()
        self.object.users.add(user)

    def post(self, request, *args, **kwargs):
        self.action()
        return redirect('projects:project_detail', pk=self.object.pk)


class ProjectDelMember(MembersOperationsMixin):
    def action(self):
        user = self.get_user()
        self.object.users.remove(user)

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.action()
        return redirect(self.get_success_url())
