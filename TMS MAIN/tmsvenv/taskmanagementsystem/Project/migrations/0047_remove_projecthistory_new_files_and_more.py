# Generated by Django 4.1.4 on 2023-11-08 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0046_projecthistory_new_files_projecthistory_new_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecthistory',
            name='new_files',
        ),
        migrations.RemoveField(
            model_name='projecthistory',
            name='old_files',
        ),
    ]
