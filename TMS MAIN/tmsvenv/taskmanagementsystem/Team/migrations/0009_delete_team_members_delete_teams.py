# Generated by Django 4.1.4 on 2023-11-13 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0055_remove_projects_team1_alter_projects_team'),
        ('Tasks', '0027_alter_projecthistory_new_team_and_more'),
        ('Team', '0008_team'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Team_members',
        ),
        migrations.DeleteModel(
            name='Teams',
        ),
    ]
