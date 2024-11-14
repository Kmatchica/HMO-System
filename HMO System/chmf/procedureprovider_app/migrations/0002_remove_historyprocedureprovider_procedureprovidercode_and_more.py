# Generated by Django 5.0.3 on 2024-10-21 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalprocedures_app', '0002_alter_medicalprocedures_procedurecode'),
        ('procedureprovider_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historyprocedureprovider',
            name='procedureprovidercode',
        ),
        migrations.AlterField(
            model_name='historyprocedureprovider',
            name='procedurecode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medicalprocedures_app.medicalprocedures', to_field='procedurecode'),
        ),
    ]
