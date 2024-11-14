from django.db import models
from provider_app.models import provider
from doctor_app.models import doctor
# Create your models here.
class providerdoctors(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     room = models.CharField(max_length=100)
     scheduleday = models.CharField(max_length=100)
     scheduletime = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="providerdoctors"#new userdatabase

class historyproviderdoctors(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
     providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
     room = models.CharField(max_length=100)
     scheduleday = models.CharField(max_length=100)
     scheduletime = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyproviderdoctors"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='providerdoctorsrecordh_idx'),
            
        ]
      