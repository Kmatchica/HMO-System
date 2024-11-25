from django.db import models
from member_app.models import member, historymember
from doctor_app.models import doctor
from provider_app.models import provider
from medicaldiagnosis_app.models import diagnosis
from medicalavailmentstatus_app.models import availmentstatus
from medicalavailmenttype_app.models import availmenttype
from django.utils.timezone import now


class approval(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    approvalcode = models.CharField(max_length=100, unique=True)
    policynumber = models.ForeignKey(member, on_delete=models.DO_NOTHING, to_field='policynumber')
    # memberrecordnohist = models.ForeignKey(historymember, on_delete=models.DO_NOTHING, to_field='recordnohist')
    availmentdate = models.DateTimeField()
    providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
    doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
    callername = models.CharField(max_length=100)
    availmenttypecode = models.ForeignKey(availmenttype, on_delete=models.DO_NOTHING, to_field='availmenttypecode')
    initialdiagnosis = models.ForeignKey(diagnosis, on_delete=models.DO_NOTHING, related_name='initialdiagnosis')
    finaldiagnosis = models.ForeignKey(diagnosis, on_delete=models.DO_NOTHING, related_name='finaldiagnosis')
    idpresented = models.CharField(max_length=100)
    statuscode = models.ForeignKey(availmentstatus, on_delete=models.DO_NOTHING, to_field='availmentstatuscode')
    disapproved = models.CharField(max_length=100)
    remarks = models.TextField()
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="approval"

class historyapproval(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    approvalcode = models.CharField(max_length=100)
    policynumber = models.ForeignKey(member, on_delete=models.DO_NOTHING, to_field='policynumber')
    # memberrecordnohist = models.ForeignKey(historymember, on_delete=models.DO_NOTHING, to_field='recordnohist')
    availmentdate = models.DateTimeField()
    providercode = models.ForeignKey(provider, on_delete=models.DO_NOTHING, to_field='providercode')
    doctorcode = models.ForeignKey(doctor, on_delete=models.DO_NOTHING, to_field='doctorcode')
    callername = models.CharField(max_length=100)
    availmenttypecode = models.ForeignKey(availmenttype, on_delete=models.DO_NOTHING, to_field='availmenttypecode')
    initialdiagnosis = models.ForeignKey(diagnosis, on_delete=models.DO_NOTHING, related_name='historyinitialdiagnosis')
    finaldiagnosis = models.ForeignKey(diagnosis, on_delete=models.DO_NOTHING, related_name='historyfinaldiagnosis')
    idpresented = models.CharField(max_length=100)
    statuscode = models.ForeignKey(availmentstatus, on_delete=models.DO_NOTHING, to_field='availmentstatuscode')
    disapproved = models.CharField(max_length=100)
    remarks = models.TextField()
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
            db_table="historyapproval"
            indexes = [
            models.Index(fields=['recordno'], name='historyapprovalh_idx'),
        ]

