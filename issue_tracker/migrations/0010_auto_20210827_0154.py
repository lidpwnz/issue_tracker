# Generated by Django 3.2.6 on 2021-08-26 19:54

from django.db import migrations, models
import django.db.models.deletion
import issue_tracker.helpers.validators


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0009_alter_issue_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='Started Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
            ],
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, null=True, validators=[issue_tracker.helpers.validators.body_at_least_7], verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='issue_tracker.status', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='summary',
            field=models.CharField(max_length=150, validators=[issue_tracker.helpers.validators.title_with_create_input], verbose_name='Summary'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='type',
            field=models.ManyToManyField(default=1, related_name='issues', to='issue_tracker.Type', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated Date'),
        ),
        migrations.AlterField(
            model_name='status',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='type',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
    ]
