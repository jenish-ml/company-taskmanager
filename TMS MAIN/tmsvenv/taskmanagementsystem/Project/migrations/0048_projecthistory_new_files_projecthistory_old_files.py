# Generated by Django 4.1.4 on 2023-11-08 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0047_remove_projecthistory_new_files_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecthistory',
            name='new_files',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='projecthistory',
            name='old_files',
            field=models.TextField(null=True),
        ),
    ]
