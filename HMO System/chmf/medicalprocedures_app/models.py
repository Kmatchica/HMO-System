from django.db import models

# Create your models here.
class medicalprocedures(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     procedurecode = models.IntegerField(unique=True)
     procedureabbreviation = models.CharField(max_length=100)
     procedurename = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="medicalprocedures"#new userdatabase

class historymedicalprocedures(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     procedurecode = models.IntegerField()
     procedureabbreviation = models.CharField(max_length=100)
     procedurename = models.CharField(max_length=100)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historymedicalprocedures"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='medicalproceduresrecordh_idx'),
            
        ]
      