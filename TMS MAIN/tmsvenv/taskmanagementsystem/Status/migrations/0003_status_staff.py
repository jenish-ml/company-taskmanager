# Generated by Django 4.1.4 on 2023-10-16 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0002_alter_status_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='staff',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
