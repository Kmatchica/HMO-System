from django.db import models
from clientclassification_app.models import clientclassification
from clientstatus_app.models import clientstatus


class client(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    clientcode = models.CharField(max_length=100, unique=True)
    clientparentcode = models.IntegerField()
    clientclassificationcode = models.ForeignKey(clientclassification, on_delete=models.DO_NOTHING, to_field='clientclassificationcode')
    clientname = models.CharField(max_length=100)
    clientshortname = models.CharField(max_length=100)
    subscriptiondate = models.DateTimeField()
    effectivedate = models.DateTimeField()
    expirydate = models.DateTimeField()
    renewaldate = models.DateTimeField()
    statuscode = models.ForeignKey(clientstatus, on_delete=models.DO_NOTHING, to_field='clientstatuscode')
    registrationnumber = models.IntegerField()
    gascheduledate = models.DateTimeField()
    tin = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    locationcode = models.IntegerField()
    contactnumber = models.CharField(max_length=100)
    emailaddress = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="client"

class historyclient(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    clientcode = models.CharField(max_length=100)
    clientparentcode = models.IntegerField()
    clientclassificationcode = models.ForeignKey(clientclassification, on_delete=models.DO_NOTHING, to_field='clientclassificationcode')
    clientname = models.CharField(max_length=100)
    clientshortname = models.CharField(max_length=100)
    subscriptiondate = models.DateTimeField()
    effectivedate = models.DateTimeField()
    expirydate = models.DateTimeField()
    renewaldate = models.DateTimeField()
    statuscode = models.ForeignKey(clientstatus, on_delete=models.DO_NOTHING, to_field='clientstatuscode')
    registrationnumber = models.IntegerField()
    gascheduledate = models.DateTimeField()
    tin = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    locationcode = models.IntegerField()
    contactnumber = models.CharField(max_length=100)
    emailaddress = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyclient"
        indexes = [
        models.Index(fields=['recordno'], name='clienth_idx'),
    ]
