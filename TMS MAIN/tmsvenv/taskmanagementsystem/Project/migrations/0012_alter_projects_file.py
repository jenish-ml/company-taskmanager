# Generated by Django 4.1.4 on 2023-10-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0011_alter_projects_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
