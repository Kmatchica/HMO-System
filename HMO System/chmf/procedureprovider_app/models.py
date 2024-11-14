from django.db import models
from provider_app.models import provider
from medicalprocedures_app.models import medicalprocedures
# Create your models here.
class procedureprovider(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     procedureprovidercode = models.IntegerField()
     procedurecode = models.ForeignKey(medicalprocedures, on_delete=models.DO_NOTHING, to_field='procedurecode')
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     amount = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="procedureprovider"#new userdatabase

class historyprocedureprovider(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     procedureprovidercode = models.IntegerField()
     procedurecode = models.ForeignKey(medicalprocedures, on_delete=models.DO_NOTHING, to_field='procedurecode')
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     amount = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyprocedureprovider"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='procedureproviderrecordh_idx'),
            
        ]
      