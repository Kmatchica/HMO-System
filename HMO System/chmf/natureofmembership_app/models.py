from django.db import models

# Create your models here.
class NatureOfMembership(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     natureofmembershipid = models.IntegerField()
     natureofmembership = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="NatureOfMembership"#new userdatabase

class historynatureofmembership(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     natureofmembershipid = models.IntegerField()
     natureofmembership = models.CharField(max_length=50)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historynatureofmembership"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='membershipidrecordh_idx'),
            
        ]
      