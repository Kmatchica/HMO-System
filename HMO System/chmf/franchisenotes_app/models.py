from django.db import models
from franchise_app.models import franchise
# Create your models here.
class franchisenotes(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     franchisenoteid = models.IntegerField()
     franchisecode = models.ForeignKey(franchise, on_delete=models.DO_NOTHING, to_field='franchisecode')
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="franchisenotes"#new userdatabase

class historyfranchisenotes(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     franchisenoteid = models.IntegerField()
     franchisecode = models.ForeignKey(franchise, on_delete=models.DO_NOTHING, to_field='franchisecode')
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100) 
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyfranchisenotes"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='franchisenoteidrecordh_idx'),
            
        ]
      