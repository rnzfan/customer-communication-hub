# Generated by Django 4.0.6 on 2022-07-28 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0002_client_task_draft_commenttask_commentdraft_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='frontpage.client'),
        ),
    ]
