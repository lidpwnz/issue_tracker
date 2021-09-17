import django_filters
from issue_tracker.models import Issue
from django import forms
from issue_tracker.models import Status, Type
from django_filters.widgets import RangeWidget


class IssueFilter(django_filters.FilterSet):
    summary = django_filters.CharFilter(lookup_expr='icontains',
                                        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
                                        label='Summary')
    description = django_filters.CharFilter(lookup_expr='icontains',
                                            widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
                                            label='Description')
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    type = django_filters.ModelChoiceFilter(queryset=Type.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-select mb-3'}))
    created_at = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'YYYY-MM-DD'}
    ))
    updated_at = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(
        attrs={'class': 'form-control form-control-sm', 'placeholder': 'YYYY-MM-DD'}
    ))

    class Meta:
        model = Issue
        exclude = ['project', 'is_deleted']
