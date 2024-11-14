from django.db import models

class availmenttype(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    availmenttypecode = models.IntegerField(unique=True)
    availmenttypename = models.CharField(max_length=100)
    availmenttypeshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="availmenttype"

class historyavailmenttype(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    availmenttypecode = models.IntegerField()
    availmenttypename = models.CharField(max_length=100)
    availmenttypeshortname = models.CharField(max_length=100)
    availmenttyperemarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyavailmenttype"
        indexes = [
        models.Index(fields=['recordno'], name='availmenttypeh_idx'),
    ]
    