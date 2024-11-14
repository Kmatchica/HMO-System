from django.db import models
from client_app.models import client

class clientsob(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    clientsobcode = models.IntegerField(unique=True)
    clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
    sobcode = models.IntegerField()
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="clientsob"

class historyclientsob(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    clientsobcode = models.IntegerField()
    clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
    sobcode = models.IntegerField()
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyclientsob"
        indexes = [
        models.Index(fields=['recordno'], name='clientsobh_idx'),
    ]
