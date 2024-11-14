from django.db import models
from medicalprocedures_app.models import medicalprocedures 
from doctor_app.models import doctor


class approvalprocedure(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    approvalcode = models.IntegerField(unique=True)
    procedurecode = models.ForeignKey(medicalprocedures, on_delete=models.DO_NOTHING, to_field='procedurecode')
    doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
    professionalfee = models.IntegerField()
    confinementamount = models.IntegerField()
    otheramount = models.IntegerField()
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="approvalprocedure"

class historyapprovalprocedure(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    approvalcode = models.IntegerField()
    procedurecode = models.ForeignKey(medicalprocedures, on_delete=models.DO_NOTHING, to_field='procedurecode')
    doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
    professionalfee = models.IntegerField()
    confinementamount = models.IntegerField()
    otheramount = models.IntegerField()
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyapprovalprocedure"
        indexes = [
        models.Index(fields=['recordno'], name='approvalprocedureh_idx'),
    ]
    