# Generated by Django 2.1.7 on 2019-02-25 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0002_anadoctasks_devdoctasks'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaDevDocTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('summary', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('team', models.CharField(max_length=50)),
                ('application', models.CharField(max_length=50)),
            ],
        ),
    ]
