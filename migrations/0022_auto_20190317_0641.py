# Generated by Django 2.1.7 on 2019-03-17 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0021_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='jira_app_desc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='jira_app_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
