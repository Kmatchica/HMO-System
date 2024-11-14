# Generated by Django 5.1 on 2024-11-12 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='saletype',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('salestypeid', models.IntegerField()),
                ('salestypename', models.CharField(max_length=100)),
                ('salestypeshortname', models.CharField(max_length=100)),
                ('commissionpercent', models.DecimalField(decimal_places=6, max_digits=18)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'saletype',
            },
        ),
        migrations.CreateModel(
            name='historysaletype',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('salestypeid', models.IntegerField()),
                ('salestypename', models.CharField(max_length=100)),
                ('salestypeshortname', models.CharField(max_length=100)),
                ('commissionpercent', models.DecimalField(decimal_places=6, max_digits=18)),
                ('remarks', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historysaletype',
                'indexes': [models.Index(fields=['recordno'], name='salestypeidrecordh_idx')],
            },
        ),
    ]
