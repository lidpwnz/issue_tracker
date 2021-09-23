import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.generic.base import ContextMixin, View
from django.urls import reverse_lazy


class AccountsMixin(ContextMixin, View):
    next_url = None

    @classmethod
    def get_next_url(cls):
        return cls.next_url

    @classmethod
    def set_next_url(cls, url):
        cls.next_url = url

    def dispatch(self, request, *args, **kwargs):
        url = self.get_next_url_from_request()
        AccountsMixin.set_next_url(url)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(next_url=self.get_next_url())

    def get_next_url_from_request(self):
        return self.request.GET.get('next', self.request.POST.get('next', ''))

    def get_success_url(self):
        return self.get_next_url() or reverse_lazy('acc:profile', kwargs={'pk': self.request.user.pk})


class DeleteOldPhotoMixin(View):
    object = None

    def delete_old_photo(self, avatar=None):
        avatar = self.request.FILES.get('avatar') if not avatar else avatar
        current_avatar = self.request.user.profile.avatar

        if avatar and current_avatar != settings.AVATARS_DEFAULT_VALUE:
            try:
                os.remove(self.object.profile.avatar.path)
            except Exception as e:
                print('Exception in removing old profile image: ', e)


class UserValidationMixin:
    cleaned_data = None

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

