# Generated by Django 4.1.4 on 2023-10-12 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0017_remove_projects_file_paths'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projects',
            old_name='files',
            new_name='file',
        ),
    ]
