from django.db import models

# Create your models here.
class doctorstatus(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     doctorstatuscode = models.IntegerField(unique=True)
     statusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="doctorstatus"#new userdatabase

class historydoctorstatus(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     doctorstatuscode = models.IntegerField()
     statusname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historydoctorstatus"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='doctorstatusrecordh_idx'),
            
        ]
      