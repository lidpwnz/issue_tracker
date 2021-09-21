from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile


def get_widget_attrs(**kwargs):
    context = {'class': 'form-control mb-3'}
    if kwargs:
        context.update(kwargs)
    return context


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
        widgets = {
            'password1': forms.PasswordInput(attrs=get_widget_attrs(type='password')),
            'password2': forms.PasswordInput(attrs=get_widget_attrs(type='password')),
            'email': forms.EmailInput(attrs=get_widget_attrs(type='email')),
        }

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if not first_name and not last_name:
            raise ValidationError('First name or last name required!')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required!')
        return email

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
            'first_name': forms.TextInput(attrs=get_widget_attrs()),
            'last_name': forms.TextInput(attrs=get_widget_attrs()),
            'email': forms.EmailInput(attrs=get_widget_attrs())
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'github_link': forms.URLInput(attrs=get_widget_attrs()),
            'personal_info': forms.Textarea(attrs=get_widget_attrs()),
            'avatar': forms.FileInput(attrs=get_widget_attrs())
        }


class UserChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs=get_widget_attrs()))
    new_password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs=get_widget_attrs()))
    confirm_new_password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs=get_widget_attrs()))

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password', 'confirm_new_password']

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise ValidationError('New passwords must be equal!')
        return confirm_new_password

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise ValidationError('Incorrect old password!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('new_password'))
        if commit:
            user.save()
        return user
