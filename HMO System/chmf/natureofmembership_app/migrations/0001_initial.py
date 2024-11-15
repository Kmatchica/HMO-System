# Generated by Django 5.0.3 on 2024-10-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='natureofmembership',
            fields=[
                ('recordno', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('natureofmembershipid', models.IntegerField()),
                ('natureofmembership', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'natureofmembership',
            },
        ),
        migrations.CreateModel(
            name='historynatureofmembership',
            fields=[
                ('recordnohist', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('recordno', models.IntegerField()),
                ('natureofmembershipid', models.IntegerField()),
                ('natureofmembership', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
                ('transactby', models.IntegerField()),
                ('transactdate', models.DateTimeField()),
                ('transactype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'historynatureofmembership',
                'indexes': [models.Index(fields=['recordno'], name='membershipidrecordh_idx')],
            },
        ),
    ]
