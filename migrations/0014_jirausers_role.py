# Generated by Django 2.1.7 on 2019-03-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0013_auto_20190303_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='jirausers',
            name='role',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]