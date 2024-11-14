from django.db import models

class availmentstatus(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    availmentstatuscode = models.IntegerField(unique=True)
    availmentstatusname = models.CharField(max_length=100)
    availmentstatusshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="availmentstatus"

class historyavailmentstatus(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    availmentstatuscode = models.IntegerField()
    availmentstatusname = models.CharField(max_length=100)
    availmentstatusshortname = models.CharField(max_length=100)
    availmentstatusremarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyavailmentstatus"
        indexes = [
        models.Index(fields=['recordno'], name='availmentstatush_idx'),
    ]
    