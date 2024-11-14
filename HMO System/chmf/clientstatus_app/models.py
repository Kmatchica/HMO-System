from django.db import models

class clientstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     clientstatuscode = models.IntegerField(unique=True)
     clientstatusname = models.CharField(max_length=100)
     clientstatusshortname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="clientstatus"#new userdatabase
     

class historyclientstatus(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    clientstatuscode = models.IntegerField(unique=True)
    clientstatusname = models.CharField(max_length=100)
    clientstatusshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyclientstatus"
        indexes = [
        models.Index(fields=['recordno'], name='clientstatush_idx'),
    ]
