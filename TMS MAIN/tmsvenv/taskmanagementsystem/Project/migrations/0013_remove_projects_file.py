# Generated by Django 4.1.4 on 2023-10-12 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0012_alter_projects_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='file',
        ),
    ]
