# Generated by Django 3.2.6 on 2021-09-22 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0017_auto_20210920_0858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('add_users_to_project', 'Able to add users to project'), ('delete_users_from_project', 'Able to delete user from project')]},
        ),
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='summary',
            field=models.CharField(max_length=150, verbose_name='Summary'),
        ),
    ]
