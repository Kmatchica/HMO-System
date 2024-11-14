# Generated by Django 5.0.2 on 2024-08-14 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='historyproviderstatus',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('providerstatuscode', models.IntegerField()),
                ('statusname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyproviderstatus',
                'indexes': [models.Index(fields=['recordno'], name='providerstatuscodenrecordh_idx')],
            },
        ),
        migrations.CreateModel(
            name='providerstatus',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('providerstatuscode', models.IntegerField(unique=True)),
                ('statusname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'providerstatus',
                'indexes': [models.Index(fields=['providerstatuscode'], name='providerstatuscode_idx'), models.Index(fields=['providerstatuscode', 'statusname'], name='statusname')],
            },
        ),
    ]
