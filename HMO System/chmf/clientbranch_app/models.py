from django.db import models
from client_app.models import client
from clientstatus_app.models import clientstatus

class branch(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    branchcode = models.IntegerField(unique=True)
    clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
    branchname = models.CharField(max_length=100)
    branchshortname = models.CharField(max_length=100)
    statuscode = models.ForeignKey(clientstatus, on_delete=models.DO_NOTHING, to_field='clientstatuscode')
    tin = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    locationcode = models.IntegerField()
    contactnumber = models.CharField(max_length=100)
    emailaddress = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="branch"

class historybranch(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    branchcode = models.IntegerField()
    clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
    branchname = models.CharField(max_length=100)
    branchshortname = models.CharField(max_length=100)
    statuscode = models.ForeignKey(clientstatus, on_delete=models.DO_NOTHING, to_field='clientstatuscode')
    tin = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    locationcode = models.IntegerField()
    contactnumber = models.CharField(max_length=100)
    emailaddress = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historybranch"
        indexes = [
        models.Index(fields=['recordno'], name='branchh_idx'),
    ]
