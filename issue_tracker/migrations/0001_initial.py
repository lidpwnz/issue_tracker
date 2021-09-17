# Generated by Django 3.2.6 on 2021-08-10 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=150, verbose_name='Краткое описание')),
                ('description', models.CharField(max_length=1000, verbose_name='Полное описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='issue_tracker.status', verbose_name='Статус')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='issue_tracker.type', verbose_name='Тип')),
            ],
        ),
    ]
