# Generated by Django 4.0 on 2024-11-20 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
