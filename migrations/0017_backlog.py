# Generated by Django 2.1.7 on 2019-03-12 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0016_auto_20190307_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=250)),
            ],
        ),
    ]
