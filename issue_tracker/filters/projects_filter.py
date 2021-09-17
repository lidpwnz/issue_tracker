import django_filters
from issue_tracker.models import Project
from django import forms
from django_filters.widgets import RangeWidget


class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
                                      label='Title')
    description = django_filters.CharFilter(lookup_expr='icontains',
                                            widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
                                            label='Description')
    create_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'YYYY-MM-DD'}
    ))
    end_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'YYYY-MM-DD'}
    ))

    class Meta:
        model = Project
        fields = ('title', 'description', 'create_date', 'end_date')
