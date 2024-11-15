# Generated by Django 5.0.2 on 2024-11-11 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='availmentstatus',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('availmentstatuscode', models.IntegerField(unique=True)),
                ('availmentstatusname', models.CharField(max_length=100)),
                ('availmentstatusshortname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'availmentstatus',
            },
        ),
        migrations.CreateModel(
            name='historyavailmentstatus',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('availmentstatuscode', models.IntegerField()),
                ('availmentstatusname', models.CharField(max_length=100)),
                ('availmentstatusshortname', models.CharField(max_length=100)),
                ('availmentstatusremarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyavailmentstatus',
                'indexes': [models.Index(fields=['recordno'], name='availmentstatush_idx')],
            },
        ),
    ]
