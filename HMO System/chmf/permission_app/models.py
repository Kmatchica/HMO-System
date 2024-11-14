from django.db import models


# Create your models here.
class permission(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     roleid = models.IntegerField()
     modulecode = models.IntegerField()
     accesscode = models.IntegerField()
     holder = models.IntegerField()
     remarks = models.CharField(max_length=100)
     class Meta:
         db_table="permission"#new userdatabase

class historypermission(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     roleid = models.IntegerField()
     modulecode = models.IntegerField()
     accesscode = models.IntegerField()
     holder = models.IntegerField()
     remarks = models.CharField(max_length=100)
     class Meta:
         db_table="historypermission"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='permissionrecordh_idx'),
            
            
        ] 