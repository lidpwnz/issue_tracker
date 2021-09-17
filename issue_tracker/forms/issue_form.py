from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms import Form
from issue_tracker.models import Issue
from django import forms


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'status', 'type', 'description']

        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Summary',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select mb-3'
            }),
            'type': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Description'
            }),
        }

    def clean_summary(self):
        data = self.cleaned_data.get('summary')
        if data == 'test':
            raise ValidationError('Invalid value for summary!', code='invalid')

        return data


class SearchForm(Form):
    search = forms.CharField(max_length=150, required=False)
