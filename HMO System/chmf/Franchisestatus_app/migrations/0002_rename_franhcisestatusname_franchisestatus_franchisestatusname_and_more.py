# Generated by Django 5.1 on 2024-11-06 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Franchisestatus_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='franchisestatus',
            old_name='franhcisestatusname',
            new_name='franchisestatusname',
        ),
        migrations.RenameField(
            model_name='historyfranchisestatus',
            old_name='franhcisestatusname',
            new_name='franchisestatusname',
        ),
    ]
