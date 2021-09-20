from django.db import models
from .helpers.validators import title_with_create_input, body_at_least_7
from django.contrib.auth import get_user_model


class Type(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, verbose_name='Title')

    def __str__(self):
        return self.title


class Issue(models.Model):
    summary = models.CharField(max_length=150, verbose_name='Summary', validators=(title_with_create_input, ))
    description = models.TextField(verbose_name='Description', validators=(body_at_least_7, ), null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1, related_name='issues',
                               verbose_name='Status')
    type = models.ManyToManyField(Type, default=1, related_name='issues',
                                  verbose_name='Type')
    project = models.ForeignKey('issue_tracker.Project', on_delete=models.CASCADE, default=1, related_name='issues',
                                verbose_name='Project')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated Date')

    def __str__(self):
        return f'{self.pk} {self.summary} {self.created_at.date()} {self.status} {self.type.all()}'


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    is_deleted = models.BooleanField(default=False)
    users = models.ManyToManyField(get_user_model(), blank=True, related_name='projects')
    create_date = models.DateField(verbose_name='Started Date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End Date')

    def __str__(self):
        return f'{self.title} {self.create_date} {self.end_date}'


# class ProjectUsers(models.Model):
#     project = models.ForeignKey('issue_tracker.Project', on_delete=models.CASCADE, related_name='users')
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='projects')
#     add_time = models.DateTimeField(auto_now_add=True)
#     del_time = models.DateTimeField(blank=True, null=True)
