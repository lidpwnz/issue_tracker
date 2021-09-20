from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if not first_name and not last_name:
            raise ValidationError('First name or last name required!')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('User already exists!')
        return username


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'github_link': forms.URLInput(attrs={'class': 'form-control mb-3'}),
            'personal_info': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control mb-3'})
        }
