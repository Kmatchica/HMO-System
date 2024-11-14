from django.db import models
from provider_app.models import provider
from medicalprocedures_app.models import medicalprocedures
# Create your models here.
class saletype(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     salestypeid = models.IntegerField()
     salestypename = models.CharField(max_length=100)
     salestypeshortname = models.CharField(max_length=100)
     commissionpercent = models.DecimalField(max_digits=18, decimal_places=6)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50) 
     class Meta:
         db_table="saletype"#new userdatabase

class historysaletype(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     salestypeid = models.IntegerField()
     salestypename = models.CharField(max_length=100)
     salestypeshortname = models.CharField(max_length=100)
     commissionpercent = models.DecimalField(max_digits=18, decimal_places=6)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50) 
     class Meta:
         db_table="historysaletype"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='salestypeidrecordh_idx'),
            
        ]
      