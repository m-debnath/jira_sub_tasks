# Generated by Django 2.1.7 on 2019-03-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0010_jiraapp_appdashurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='devtasks',
            name='hours',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]