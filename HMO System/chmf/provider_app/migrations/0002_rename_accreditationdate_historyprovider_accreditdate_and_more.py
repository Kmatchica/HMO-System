# Generated by Django 5.0.2 on 2024-08-14 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historyprovider',
            old_name='accreditationdate',
            new_name='accreditdate',
        ),
        migrations.RenameField(
            model_name='historyprovider',
            old_name='disaccreditationdate',
            new_name='disaccreditdate',
        ),
        migrations.RenameField(
            model_name='historyprovider',
            old_name='reaccreditationdate',
            new_name='reaccreditdate',
        ),
        migrations.RenameField(
            model_name='provider',
            old_name='accreditationdate',
            new_name='accreditdate',
        ),
        migrations.RenameField(
            model_name='provider',
            old_name='disaccreditationdate',
            new_name='disaccreditdate',
        ),
        migrations.RenameField(
            model_name='provider',
            old_name='reaccreditationdate',
            new_name='reaccreditdate',
        ),
    ]
