# Generated by Django 5.0.3 on 2024-10-21 01:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicalprocedures_app', '0002_alter_medicalprocedures_procedurecode'),
        ('provider_app', '0002_rename_accreditationdate_historyprovider_accreditdate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='historyprocedureprovider',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('procedureprovidercode', models.IntegerField()),
                ('procedurecode', models.IntegerField()),
                ('providercode', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historyprocedureprovider',
                'indexes': [models.Index(fields=['recordno'], name='procedureproviderrecordh_idx')],
            },
        ),
        migrations.CreateModel(
            name='procedureprovider',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('procedureprovidercode', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
                ('procedurecode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicalprocedures_app.medicalprocedures', to_field='procedurecode')),
                ('providercode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='provider_app.provider', to_field='providercode')),
            ],
            options={
                'db_table': 'procedureprovider',
            },
        ),
    ]
