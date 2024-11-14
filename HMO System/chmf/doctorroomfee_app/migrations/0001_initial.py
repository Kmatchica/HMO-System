# Generated by Django 5.0.3 on 2024-10-22 01:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor_app', '0003_doctor_accreditdate_doctor_disaccreditdate_and_more'),
        ('roomtype_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctorroomfee',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('doctorroomfeecode', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
                ('doctorcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctor_app.doctor', to_field='doctorcode')),
                ('roomcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='roomtype_app.roomtype', to_field='roomcode')),
            ],
            options={
                'db_table': 'doctorroomfee',
            },
        ),
        migrations.CreateModel(
            name='historydoctorroomfee',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('doctorroomfeecode', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
                ('doctorcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='doctor_app.doctor', to_field='doctorcode')),
                ('roomcode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='roomtype_app.roomtype', to_field='roomcode')),
            ],
            options={
                'db_table': 'historydoctorroomfee',
                'indexes': [models.Index(fields=['recordno'], name='doctorroomfeerecordh_idx')],
            },
        ),
    ]
