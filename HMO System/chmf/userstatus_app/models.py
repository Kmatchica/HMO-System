from django.db import models


class userstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     userstatuscode = models.IntegerField()
     userstatusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="userstatus"#new userdatabase
      
         
      

class historyuserstatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     userstatuscode = models.IntegerField()
     userstatusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyuserstatus"
         indexes = [
            models.Index(fields=['recordno'], name='userstatusnrecordh_idx'),
            
        ]

