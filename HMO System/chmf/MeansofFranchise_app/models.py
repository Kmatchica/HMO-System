from django.db import models

# Create your models here.
class MeansofFranchise(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     meansofknowingid = models.IntegerField(unique=True)
     means = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="MeansofFranchise"#new userdatabase

class historymeansoffranchise(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     meansofknowingid = models.IntegerField()
     means = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historymeansoffranchise"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='meansofknowingidrecordh_idx'),
            
        ]
      