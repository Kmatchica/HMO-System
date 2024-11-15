# Generated by Django 5.0.2 on 2024-11-11 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='availmenttype',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('availmenttypecode', models.IntegerField(unique=True)),
                ('availmenttypename', models.CharField(max_length=100)),
                ('availmenttypeshortname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'availmenttype',
            },
        ),
        migrations.CreateModel(
            name='historyavailmenttype',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('availmenttypecode', models.IntegerField()),
                ('availmenttypename', models.CharField(max_length=100)),
                ('availmenttypeshortname', models.CharField(max_length=100)),
                ('availmenttyperemarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyavailmenttype',
                'indexes': [models.Index(fields=['recordno'], name='availmenttypeh_idx')],
            },
        ),
    ]
