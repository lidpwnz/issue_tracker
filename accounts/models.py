from django.db import models
from django.contrib.auth import get_user_model

avatars_folder = 'user_avatars'
avatar_default_value = f"{avatars_folder}/imageNotAvailable_grid.png"


class Profile(models.Model):
    avatar = models.ImageField(blank=True, upload_to=avatars_folder, default=avatar_default_value)
    github_link = models.URLField(null=True, blank=True)
    personal_info = models.TextField(null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
