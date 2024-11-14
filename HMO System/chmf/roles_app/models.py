from django.db import models


class roles(models.Model):
 
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    roleid = models.IntegerField(unique=True)
    rolename= models.CharField(max_length=200)
    roledisplayname = models.CharField(max_length=200)
    roledescription = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="roles"

class historyroles(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno =  models.IntegerField()
    roleid =  models.IntegerField()
    rolename= models.CharField(max_length=200)
    roledisplayname = models.CharField(max_length=200)
    roledescription = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyroles"       
    indexes = [
            models.Index(fields=['recordno'], name='rolesrecordh_idx'),
            
        ]
