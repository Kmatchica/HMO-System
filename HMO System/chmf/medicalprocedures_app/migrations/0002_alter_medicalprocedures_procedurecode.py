# Generated by Django 5.0.3 on 2024-10-21 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalprocedures_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalprocedures',
            name='procedurecode',
            field=models.IntegerField(unique=True),
        ),
    ]