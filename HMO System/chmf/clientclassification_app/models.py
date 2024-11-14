from django.db import models

# Create your models here.
class clientclassification(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     clientclassificationcode = models.IntegerField(unique=True)
     clientclassificationname = models.CharField(max_length=100)
     clientclassificationremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="clientclassification"#new userdatabase
     

class historyclientclassification(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     clientclassificationcode = models.IntegerField()
     clientclassificationname = models.CharField(max_length=100)
     clientclassificationremarks = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyclientclassification"
         indexes = [
            models.Index(fields=['recordno'], name='clientclassificationh_idx'),
        ]
