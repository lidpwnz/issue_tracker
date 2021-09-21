from abc import abstractmethod
from django.db.models import Q      # Нужно для работоспособности SearchView
from django.http import Http404
from django.shortcuts import render
from django.utils.http import urlencode
from django.views.generic import ListView
from django.views import View
from issue_tracker.filters.projects_filter import ProjectFilter
from issue_tracker.forms.issue_form import SearchForm
from issue_tracker.models import Project
from django.contrib.auth.models import User


class BaseListView(ListView):
    query = None
    search_value = None
    form = SearchForm
    template_name = 'projects/list.html'
    model = Project
    context_object_name = 'projects'
    ordering = ['-create_date']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search_value = self.get_search_value()
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return render(request, 'errors/404.html')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.search_value:
            context['query'] = urlencode({'params': self.search_value})
        return context

    def get_search_value(self):
        form = self.form(self.request.GET)
        if form.is_valid():
            return self.request.GET.get('params')


class SearchView(BaseListView):
    """
        Чтобы выбрать нужный оператор (OR/AND/NOT)
        нужно поставить соответствующий знак перед названием поля
        ("|description" к примеру)

        ======
        Если поставить оператор перед первым полем
        в массиве search_fields, то он будет проигнорирован и удален
        ======

        Параметры классов-наследников со значениями
            search_fields = ['summary', '|~description']
            search_fields_methods = ['icontains', 'icontains']

        будет эквивалентно запросу
        Q(summary__icontains=self.search_value) | ~Q(description__icontains=self.search_value)
    """
    search_fields: list = None
    search_fields_methods: list = None

    def get(self, request, *args, **kwargs):
        if not len(self.search_fields) == len(self.search_fields_methods):
            raise AttributeError('fields and methods lists must be equal!')
        return super(SearchView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        if self.search_value:
            queryset = queryset.filter(self.get_db_request()).distinct()

        return queryset
    
    def get_context_data(self, *, object_list=None, **kwargs):
        return super(SearchView, self).get_context_data(my_filter=ProjectFilter, btn_text='Filter')

    def get_q_object(self, field, method):
        return f'Q({field}__{method}="{self.search_value}")'

    def get_db_request(self):
        db_requests_list = [self.get_q_object(self.search_fields[0].strip('|&'),
                                              self.search_fields_methods[0])]

        for field, method in zip(self.search_fields[1:], self.search_fields_methods[1:]):
            field = list(field)
            operator = field.pop(0)
            tilda = field.pop(0) if field[0] == '~' else ''
            q_object = self.get_q_object(''.join(field), method)
            db_requests_list.append(f' {operator} {tilda}{q_object}')

        return eval(''.join(db_requests_list))


class MembersOperationsMixin(View):
    object = None
    model = Project

    def get_project(self):
        pk = self.kwargs.get('project_pk')
        return self.model.objects.get(pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_project()
        return super().dispatch(request, *args, **kwargs)

    def get_user(self):
        pk = self.request.POST.get('user', self.request.GET.get('user', ''))
        return User.objects.get(pk=pk)

    @abstractmethod
    def action(self):
        raise NotImplementedError
