# Generated by Django 2.1.7 on 2019-02-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_sub_tasks', '0006_anador_devanador_devdor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnaDOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('checked', models.CharField(max_length=10)),
                ('mandatory', models.CharField(max_length=10)),
                ('option', models.CharField(max_length=10)),
                ('id_1', models.CharField(max_length=10)),
                ('rank', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DevAnaDOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('checked', models.CharField(max_length=10)),
                ('mandatory', models.CharField(max_length=10)),
                ('option', models.CharField(max_length=10)),
                ('id_1', models.CharField(max_length=10)),
                ('rank', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DevDOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('checked', models.CharField(max_length=10)),
                ('mandatory', models.CharField(max_length=10)),
                ('option', models.CharField(max_length=10)),
                ('id_1', models.CharField(max_length=10)),
                ('rank', models.CharField(max_length=10)),
            ],
        ),
    ]
