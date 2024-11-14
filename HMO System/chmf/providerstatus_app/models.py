from django.db import models


class providerstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     providerstatuscode = models.IntegerField(unique=True)
     statusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="providerstatus"#new userdatabase
         indexes = [
            models.Index(fields=['providerstatuscode'], name='providerstatuscode_idx'),
            models.Index(fields=['providerstatuscode', 'statusname'], name='statusname'),
        ]
      
         
      

class historyproviderstatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     providerstatuscode = models.IntegerField()
     statusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyproviderstatus"
         indexes = [
            models.Index(fields=['recordno'], name='providerstatuscodenrecordh_idx'),
     
            
        ]

