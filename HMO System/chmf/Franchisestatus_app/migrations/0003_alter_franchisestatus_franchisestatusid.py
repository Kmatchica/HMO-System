# Generated by Django 5.1 on 2024-11-13 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Franchisestatus_app', '0002_rename_franhcisestatusname_franchisestatus_franchisestatusname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franchisestatus',
            name='franchisestatusid',
            field=models.IntegerField(unique=True),
        ),
    ]