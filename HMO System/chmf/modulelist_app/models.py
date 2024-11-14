from django.db import models

# Create your models here.
class moduleslist(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     modulecode = models.IntegerField()
     modulename = models.CharField(max_length=100)
     moduleshortname = models.CharField(max_length=100)
     moduleappname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status= models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="moduleslist"#new userdatabase
      

class historymoduleslist(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     modulecode = models.IntegerField()
     modulename = models.CharField(max_length=100)
     moduleshortname = models.CharField(max_length=100)
     moduleappname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status= models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historymoduleslist"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='moduleslistrecordh_idx'),
            
        ]
      