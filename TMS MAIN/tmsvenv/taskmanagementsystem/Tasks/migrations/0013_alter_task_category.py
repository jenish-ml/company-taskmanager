# Generated by Django 4.1.4 on 2023-11-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0012_task_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
