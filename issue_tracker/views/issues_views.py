from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView, CreateView, DetailView, ListView, UpdateView, DeleteView
from issue_tracker.models import Issue, Project
from issue_tracker.forms.issue_form import IssueForm
from issue_tracker.filters.issues_filter import IssueFilter
from issue_tracker.helpers.services import IssueUserPassesTestMixin


class IssuesRedirect(RedirectView):
    pattern_name = 'issues:issues_list'


class IssuesList(ListView):
    template_name = 'issues/list.html'
    filter_object = None
    model = Issue
    context_object_name = 'issues'
    ordering = ['-created_at']
    extra_context = {'btn_text': 'Filter'}
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.filter_object = self.get_filter_object()
        return super(IssuesList, self).get(request, *args, **kwargs)

    def get_user_issues(self):
        return self.model.objects.filter(project__users=self.request.user, is_deleted=False)

    def get_filter_object(self):
        return IssueFilter(self.request.GET, queryset=self.get_user_issues())

    def get_queryset(self):
        return self.filter_object.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        return super(IssuesList, self).get_context_data(my_filter=self.get_filter_object())


class IssueCreate(PermissionRequiredMixin, CreateView):
    template_name = 'issues/issue.html'
    extra_context = {'btn_text': 'Create Issue'}
    model = Issue
    form_class = IssueForm
    permission_required = 'issue_tracker.add_issue'
    
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(IssueCreate, self).form_valid(form)

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs.get('project_pk'))

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.object.project.pk})


class IssueDetail(IssueUserPassesTestMixin, PermissionRequiredMixin, DetailView):
    model = Issue
    template_name = 'issues/detail.html'
    context_object_name = 'issue'
    permission_required = 'issue_tracker.view_issue'


class IssueEdit(IssueUserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'issues/issue.html'
    form_class = IssueForm
    model = Issue
    context_object_name = 'issue'
    extra_context = {'btn_text': 'edit issue'}
    permission_required = 'issue_tracker.change_issue'

    def get_success_url(self):
        return reverse('issues:issues_detail', kwargs={'pk': self.object.pk})


class IssueDelete(IssueUserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Issue
    success_url = reverse_lazy('issues:issues_list')
    permission_required = 'issue_tracker.delete_issue'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect('issues:issues_list')

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.project_id})
