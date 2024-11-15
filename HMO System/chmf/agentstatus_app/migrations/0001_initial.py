# Generated by Django 5.1 on 2024-11-12 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='agentstatus',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('agentstatusid', models.IntegerField()),
                ('agentstatusname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'agentstatus',
            },
        ),
        migrations.CreateModel(
            name='historyagentstatus',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('agentstatusid', models.IntegerField()),
                ('agentstatusname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyagentstatus',
                'indexes': [models.Index(fields=['recordno'], name='agentstatusidrecordh_idx')],
            },
        ),
    ]
