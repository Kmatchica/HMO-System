from django.db import models

# Create your models here.
class specialization(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     specializationcode = models.IntegerField(unique=True)
     specializationname = models.CharField(max_length=100)
     specializationshortname = models.CharField(max_length=100)
     remarks= models.CharField(max_length=100)
     status= models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="specialization"#new userdatabase

class historyspecialization(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     specializationcode = models.IntegerField()
     specializationname = models.CharField(max_length=100)
     specializationshortname = models.CharField(max_length=100)
     remarks= models.CharField(max_length=100)
     status= models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyspecialization"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='specializationrecordh_idx'),
            
        ] 