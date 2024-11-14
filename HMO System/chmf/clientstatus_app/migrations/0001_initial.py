# Generated by Django 5.0.3 on 2024-11-06 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clientstatus',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('clientstatuscode', models.IntegerField()),
                ('clientstatusname', models.CharField(max_length=100)),
                ('clientstatusshortname', models.CharField(max_length=100)),
                ('clientstatusremarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'clientstatus',
            },
        ),
        migrations.CreateModel(
            name='historyclientstatus',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('clientstatuscode', models.IntegerField()),
                ('clientstatusname', models.CharField(max_length=100)),
                ('clientstatusshortname', models.CharField(max_length=100)),
                ('clientstatusremarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyclientstatus',
                'indexes': [models.Index(fields=['recordno'], name='clientstatush_idx')],
            },
        ),
    ]