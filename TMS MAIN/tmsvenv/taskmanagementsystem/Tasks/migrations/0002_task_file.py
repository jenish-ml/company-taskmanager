# Generated by Django 4.1.4 on 2023-10-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0005_alter_uploadfile_file'),
        ('Tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.ManyToManyField(blank=True, to='Files.uploadfile'),
        ),
    ]
