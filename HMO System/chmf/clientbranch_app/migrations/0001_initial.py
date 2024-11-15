# Generated by Django 5.0.3 on 2024-11-07 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clientbranch',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('clientbranchcode', models.IntegerField()),
                ('clientbranchclientcode', models.IntegerField()),
                ('clientbranchname', models.CharField(max_length=100)),
                ('clientbranchshortname', models.CharField(max_length=100)),
                ('clientbranchstatuscode', models.IntegerField()),
                ('clientbranchtin', models.CharField(max_length=100)),
                ('clientbranchaddress', models.CharField(max_length=255)),
                ('clientbranchlocationcode', models.IntegerField()),
                ('clientbranchcontactnumber', models.CharField(max_length=100)),
                ('clientbranchemailaddress', models.CharField(max_length=100)),
                ('clientbranchremarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'clientbranch',
            },
        ),
        migrations.CreateModel(
            name='historyclientbranch',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('clientbranchcode', models.IntegerField()),
                ('clientbranchclientcode', models.IntegerField()),
                ('clientbranchname', models.CharField(max_length=100)),
                ('clientbranchshortname', models.CharField(max_length=100)),
                ('clientbranchstatuscode', models.IntegerField()),
                ('clientbranchtin', models.CharField(max_length=100)),
                ('clientbranchaddress', models.CharField(max_length=255)),
                ('clientbranchlocationcode', models.IntegerField()),
                ('clientbranchcontactnumber', models.CharField(max_length=100)),
                ('clientbranchemailaddress', models.CharField(max_length=100)),
                ('clientbranchremarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyclientbranch',
                'indexes': [models.Index(fields=['recordno'], name='clientbranchh_idx')],
            },
        ),
    ]
