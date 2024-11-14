from django.db import models

# Create your models here.
class Franchisestatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     franchisestatusid = models.IntegerField(unique=True)
     franchisestatusname = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="Franchisestatus"#new userdatabase

class historyfranchisestatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     franchisestatusid = models.IntegerField()
     franchisestatusname = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyfranchisestatus"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='franchisestatusidrecordh_idx'),
            
        ]
    