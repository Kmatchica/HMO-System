# Generated by Django 5.0.2 on 2024-11-13 01:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_app', '0002_alter_client_clientcode_and_more'),
        ('clientsob_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientsob',
            old_name='clientsobremarks',
            new_name='remarks',
        ),
        migrations.RenameField(
            model_name='clientsob',
            old_name='clientsobclientcode',
            new_name='sobcode',
        ),
        migrations.RenameField(
            model_name='historyclientsob',
            old_name='clientsobremarks',
            new_name='remarks',
        ),
        migrations.RenameField(
            model_name='historyclientsob',
            old_name='clientsobclientcode',
            new_name='sobcode',
        ),
        migrations.RemoveField(
            model_name='clientsob',
            name='clientsobsobcode',
        ),
        migrations.RemoveField(
            model_name='historyclientsob',
            name='clientsobsobcode',
        ),
        migrations.AddField(
            model_name='clientsob',
            name='clientcode',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='client_app.client', to_field='clientcode'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historyclientsob',
            name='clientcode',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='client_app.client', to_field='clientcode'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clientsob',
            name='clientsobcode',
            field=models.IntegerField(unique=True),
        ),
    ]
