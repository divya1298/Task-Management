# Generated by Django 4.2.14 on 2024-07-21 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0002_remove_task_created_at_remove_task_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('action_taken', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tasks.task')),
            ],
        ),
    ]
