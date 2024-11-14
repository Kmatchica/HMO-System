from django.db import models

class membergender(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     membergendercode = models.IntegerField(unique=True)
     membergendername = models.CharField(max_length=100)
     membergendershortname = models.CharField(max_length=100)
     membergenderremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="membergender"
     

class historymembergender(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     membergendercode = models.IntegerField()
     membergendername = models.CharField(max_length=100)
     membergendershortname = models.CharField(max_length=100)
     membergenderremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historymembergender"
         indexes = [
            models.Index(fields=['recordno'], name='membergenderh_idx'),
        ]
