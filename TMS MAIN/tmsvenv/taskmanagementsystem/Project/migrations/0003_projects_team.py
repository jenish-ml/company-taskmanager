# Generated by Django 4.1.4 on 2023-10-10 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0002_team_members'),
        ('Project', '0002_rename_currentdate_projects_current_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Team.teams'),
        ),
    ]
