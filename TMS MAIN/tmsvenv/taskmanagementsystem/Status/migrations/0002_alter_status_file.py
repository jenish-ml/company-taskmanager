# Generated by Django 4.1.4 on 2023-10-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Files', '0006_remove_uploadfile_project'),
        ('Status', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='file',
            field=models.ManyToManyField(blank=True, to='Files.uploadfile'),
        ),
    ]
