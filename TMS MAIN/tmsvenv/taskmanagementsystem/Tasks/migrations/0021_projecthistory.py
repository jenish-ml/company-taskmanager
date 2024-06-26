# Generated by Django 4.1.4 on 2023-11-10 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0007_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Project', '0052_delete_projecthistory'),
        ('Tasks', '0020_taskhistory_subtask_add_taskhistory_subtask_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('old_title', models.CharField(max_length=50, null=True)),
                ('new_title', models.CharField(max_length=50, null=True)),
                ('old_description', models.TextField(null=True)),
                ('new_description', models.TextField(null=True)),
                ('old_start_date', models.DateField(null=True)),
                ('new_start_date', models.DateField(null=True)),
                ('old_due_date', models.DateField(null=True)),
                ('new_due_date', models.DateField(null=True)),
                ('new_current_date', models.DateField(null=True)),
                ('old_files', models.TextField(null=True)),
                ('new_files', models.TextField(null=True)),
                ('file_status', models.TextField(null=True)),
                ('file_remove_status', models.TextField(null=True)),
                ('task_add', models.TextField(null=True)),
                ('task_delete', models.TextField(null=True)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('new_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_history_new_team', to='Team.team_members')),
                ('old_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_history_old_team', to='Team.team_members')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.projects')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Tasks.task')),
            ],
        ),
    ]
