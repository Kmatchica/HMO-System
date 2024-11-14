from django.db import models

# Create your models here.
class access(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     accesscode = models.IntegerField()
     accessname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="access"#new userdatabase
      

class historyaccess(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     accesscode = models.IntegerField()
     accessname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyaccess"
         indexes = [
            models.Index(fields=['recordno'], name='accessnrecordh_idx'),
            
        ]

