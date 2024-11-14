from django.db import models
# Create your models here.
class category(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     categorycode = models.IntegerField(unique=True)
     providercategoryname = models.CharField(max_length=100)
     providercategoryshortname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     ordernumber = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)

     class Meta:
         db_table="category"#new userdatabase
         indexes = [
            models.Index(fields=['categorycode'], name='categorycodecode_idx'),
            models.Index(fields=['categorycode', 'providercategoryname'], name='providercategoryname'),
        ]
         
class historycategory(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     categorycode = models.IntegerField()
     providercategoryname = models.CharField(max_length=100)
     providercategoryshortname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     ordernumber = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historycategory"
         indexes = [
            models.Index(fields=['recordno'], name='categoryrecordh_idx'),
            models.Index(fields=['categorycode'], name='categorycode_idx'),
            models.Index(fields=['categorycode', 'providercategoryname'], name='providercategorynameh'),
            
        ]
