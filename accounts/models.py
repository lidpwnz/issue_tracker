from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class Profile(models.Model):
    avatar = models.ImageField(blank=True, upload_to=settings.AVATARS_FOLDER, default=settings.AVATARS_DEFAULT_VALUE)
    github_link = models.URLField(null=True, blank=True)
    personal_info = models.TextField(null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
