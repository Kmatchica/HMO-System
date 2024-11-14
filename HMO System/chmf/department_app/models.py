from django.db import models

# Create your models here.
class department(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     departmentcode = models.IntegerField(unique=True)
     departmentname = models.CharField(max_length=100)
     departmentshortname = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="department"#new userdatabase
      
         
      

class historydepartment(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno =  models.IntegerField()
    departmentcode = models.IntegerField()
    departmentname = models.CharField(max_length=100)
    departmentshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
         db_table="historydepartment"
         indexes = [
            models.Index(fields=['recordno'], name='departmetnrecordh_idx'),
            
        ]

