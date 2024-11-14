from django.db import models
from doctorstatus_app.models import doctorstatus
from provider_app.models import provider
from specialization_app.models import specialization
# Create your models here.
class doctor(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     doctorcode = models.IntegerField(unique=True)
     specializationcode = models.ForeignKey(specialization, on_delete=models.DO_NOTHING, to_field='specializationcode')
     subspecializationcode= models.IntegerField()
     firstname = models.CharField(max_length=100)
     middlename = models.CharField(max_length=100)
     lastname = models.CharField(max_length=100)
     mobilenumber = models.CharField(max_length=100)
     landlinenumber = models.CharField(max_length=100)
     emailaddres = models.CharField(max_length=100)
     address = models.CharField(max_length=100, blank=True)
     locationcode= models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='locationcode')
     professionalfee = models.CharField(max_length=100)
     doctorstatuscode= models.ForeignKey(doctorstatus, on_delete=models.DO_NOTHING, to_field='doctorstatuscode')
     accreditdate = models.DateField(null=True, blank=True)
     disaccreditdate = models.DateField(null=True, blank=True)
     reaccreditdate = models.DateField(null=True, blank=True)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="doctor"#new userdatabase

class historydoctor(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno =  models.IntegerField()
     doctorcode = models.CharField(max_length=100)
     specializationcode = models.ForeignKey(specialization, on_delete=models.DO_NOTHING, to_field='specializationcode')
     subspecializationcode= models.IntegerField()
     firstname = models.CharField(max_length=100)
     middlename = models.CharField(max_length=100)
     lastname = models.CharField(max_length=100)
     mobilenumber = models.CharField(max_length=100)
     landlinenumber = models.CharField(max_length=100)
     emailaddres = models.CharField(max_length=100)
     address = models.CharField(max_length=100)
     locationcode= models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='locationcode')
     professionalfee = models.CharField(max_length=100)
     doctorstatuscode= models.ForeignKey(doctorstatus, on_delete=models.DO_NOTHING, to_field='doctorstatuscode')
     accreditdate = models.DateField(null=True, blank=True)
     disaccreditdate = models.DateField(null=True, blank=True)
     reaccreditdate = models.DateField(null=True, blank=True)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historydoctor"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='doctorrecordh_idx'),
            
        ]
      