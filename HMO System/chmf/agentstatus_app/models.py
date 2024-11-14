from django.db import models


class agentstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     agentstatusid = models.IntegerField()
     agentstatusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="agentstatus"#new userdatabase
      
      
      

class historyagentstatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     agentstatusid = models.IntegerField()
     agentstatusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyagentstatus"
         indexes = [
            models.Index(fields=['recordno'], name='agentstatusidrecordh_idx'),
     
            
        ]

