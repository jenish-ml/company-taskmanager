# Generated by Django 4.1.4 on 2023-11-08 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0006_alter_status_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='current_status',
        ),
    ]
