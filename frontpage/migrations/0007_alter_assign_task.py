# Generated by Django 4.0.6 on 2022-08-01 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0006_task_snippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assign',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.task', unique=True),
        ),
    ]
