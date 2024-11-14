from django.db import models
from roomtype_app.models import roomtype
from doctor_app.models import doctor
# Create your models here.
class doctorroomfee(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     doctorroomfeecode = models.IntegerField()
     doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
     roomcode = models.ForeignKey(roomtype, on_delete=models.DO_NOTHING, to_field='roomcode')
     amount = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="doctorroomfee"#new userdatabase

class historydoctorroomfee(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     doctorroomfeecode = models.IntegerField()
     doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
     roomcode = models.ForeignKey(roomtype, on_delete=models.DO_NOTHING, to_field='roomcode')
     amount = models.IntegerField()
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historydoctorroomfee"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='doctorroomfeerecordh_idx'),
            
        ]
      