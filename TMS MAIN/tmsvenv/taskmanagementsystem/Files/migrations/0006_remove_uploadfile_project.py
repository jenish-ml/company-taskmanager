# Generated by Django 4.1.4 on 2023-10-14 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0005_alter_uploadfile_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadfile',
            name='project',
        ),
    ]
