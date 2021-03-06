# Generated by Django 3.2.6 on 2021-08-19 11:17

from django.db import migrations, models
import issue_tracker.helpers.validators


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0008_auto_20210817_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, null=True, validators=[issue_tracker.helpers.validators.body_at_least_7], verbose_name='Полное описание'),
        ),
    ]
