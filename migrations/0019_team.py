# Generated by Django 2.1.7 on 2019-03-17 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0018_clarifyanalysistask_clarifyapp_clarifyappinfo_clarifydevtask_clarifydod_clarifydor_clarifylabel_clar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30)),
                ('jira_id', models.CharField(max_length=30)),
                ('jira_desc', models.CharField(max_length=50)),
            ],
        ),
    ]
