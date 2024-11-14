from django.db import models

class memberstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     memberstatuscode = models.IntegerField(unique=True)
     memberstatusname = models.CharField(max_length=100)
     memberstatusshortname = models.CharField(max_length=100)
     memberstatusremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="memberstatus"
     

class historymemberstatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     memberstatuscode = models.IntegerField()
     memberstatusname = models.CharField(max_length=100)
     memberstatusshortname = models.CharField(max_length=100)
     memberstatusremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historymemberstatus"
         indexes = [
            models.Index(fields=['recordno'], name='memberstatush_idx'),
        ]
