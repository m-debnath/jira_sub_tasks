# Generated by Django 2.1.7 on 2019-03-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0012_auto_20190303_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysistasks',
            name='hours',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='analysistasks',
            name='hoursDesc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devtasks',
            name='hoursDesc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='testtasks',
            name='hours',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='testtasks',
            name='hoursDesc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
