# Generated by Django 4.0.6 on 2022-08-10 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0009_alter_commenttask_task'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commenttask',
            options={'ordering': ['-time_commented']},
        ),
    ]
