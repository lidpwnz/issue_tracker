from django.forms.models import ModelForm
from issue_tracker.models import Project
from django import forms
from datetime import date


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['is_deleted', 'users']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3'
            }),
            'create_date': forms.TextInput(attrs={
                'type': 'date',
                'class': 'form-control mb-3',
                'min': date.today()
            }),
            'end_date': forms.TextInput(attrs={
                'type': 'date',
                'class': 'form-control mb-3',
                'min': date.today()
            })
        }

