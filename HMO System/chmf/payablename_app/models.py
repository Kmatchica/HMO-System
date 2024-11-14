from django.db import models
from provider_app.models import provider
# Create your models here.
class payableName(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     payablenameid = models.IntegerField()
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     payablename = models.CharField(max_length=100)
     tin = models.CharField(max_length=100)
     daystype = models.CharField(max_length=100)
     numberofdays = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="payableName"#new userdatabase

class historypayableName(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno =  models.IntegerField()
     payablenameid = models.IntegerField()
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     payablename = models.CharField(max_length=100)
     tin = models.CharField(max_length=100)
     daystype = models.CharField(max_length=100)
     numberofdays = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historypayableName"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='payableNamerecordh_idx'),
            
        ]
      