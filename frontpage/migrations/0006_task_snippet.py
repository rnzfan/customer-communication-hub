# Generated by Django 4.0.6 on 2022-07-29 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0005_task_gmail_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='snippet',
            field=models.TextField(blank=True),
        ),
    ]
