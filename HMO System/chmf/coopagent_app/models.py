from django.db import models
from department_app.models import department
from roles_app.models import roles

class coopagent(models.Model):
    # id=models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    agentid= models.IntegerField()
    firstname= models.CharField(max_length=200)
    middlename= models.CharField(max_length=200)
    lastname= models.CharField(max_length=200)
    suffix = models.CharField(max_length=200)
    civilstatuscode = models.CharField(max_length=200)
    birthdate = models.DateField()
    email = models.CharField(max_length=200)
    departmentcode = models.ForeignKey(department, on_delete=models.DO_NOTHING, to_field='departmentcode', blank=True)
    roleid = models.ForeignKey(roles, on_delete=models.DO_NOTHING, to_field='roleid', blank=True)
    mobilenumber = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    locationcode= models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    status= models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="coopagent"


class historycoopagent(models.Model):
    # id=models.BigAutoField(auto_created=True, primary_key=True)
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    agentid= models.IntegerField()
    firstname= models.CharField(max_length=200)
    middlename= models.CharField(max_length=200)
    lastname= models.CharField(max_length=200)
    suffix = models.CharField(max_length=200)
    civilstatuscode = models.CharField(max_length=200)
    birthdate = models.DateField()
    email = models.CharField(max_length=200)
    departmentcode = models.ForeignKey(department, on_delete=models.DO_NOTHING, to_field='departmentcode', blank=True)
    roleid = models.ForeignKey(roles, on_delete=models.DO_NOTHING, to_field='roleid', blank=True)
    mobilenumber = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    locationcode= models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    status= models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historycoopagent"
        indexes = [
            models.Index(fields=['recordno'], name='coopagentrecordh_idx'),
            
        ]

