# Generated by Django 5.0.2 on 2024-11-12 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor_app', '0004_doctor_subspecializationcode_and_more'),
        ('medicalprocedures_app', '0002_alter_medicalprocedures_procedurecode'),
    ]

    operations = [
        migrations.CreateModel(
            name='approvalprocedure',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('approvalcode', models.IntegerField(unique=True)),
                ('professionalfee', models.IntegerField()),
                ('confinementamount', models.IntegerField()),
                ('otheramount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
                ('doctorcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctor_app.doctor', to_field='doctorcode')),
                ('procedurecode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicalprocedures_app.medicalprocedures', to_field='procedurecode')),
            ],
            options={
                'db_table': 'approvalprocedure',
            },
        ),
        migrations.CreateModel(
            name='historyapprovalprocedure',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('approvalcode', models.IntegerField()),
                ('procedurename', models.CharField(max_length=100)),
                ('procedureshortname', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
                ('doctorcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctor_app.doctor', to_field='doctorcode')),
                ('procedurecode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicalprocedures_app.medicalprocedures', to_field='procedurecode')),
            ],
            options={
                'db_table': 'historyapprovalprocedure',
                'indexes': [models.Index(fields=['recordno'], name='approvalprocedureh_idx')],
            },
        ),
    ]
