# Generated by Django 3.2.6 on 2021-08-26 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0010_auto_20210827_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='issue_tracker.project', verbose_name='Project'),
        ),
    ]
