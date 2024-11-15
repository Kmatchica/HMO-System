from django.db import models
from membergender_app.models import membergender
from memberstatus_app.models import memberstatus
from client_app.models import client
from clientbranch_app.models import branch
class member(models.Model):
        recordno = models.BigAutoField(auto_created=True, primary_key=True)
        membercode = models.CharField(max_length=100, unique=True)
        policynumber = models.CharField(max_length=255, unique=True)
        thirdpartyid = models.CharField(max_length=255)
        otherid = models.CharField(max_length=255)
        clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
        branchcode = models.IntegerField()
        membertypecode = models.IntegerField()
        lastname = models.CharField(max_length=255)
        firstname = models.CharField(max_length=255)
        middlename = models.CharField(max_length=255)
        birthdate = models.DateField()
        enrollage = models.DecimalField(max_digits=10, decimal_places=2)
        gendercode = models.ForeignKey(membergender, on_delete=models.DO_NOTHING, to_field='membergendercode')
        civilstatuscode = models.IntegerField()
        effectivedate = models.DateTimeField()
        expirydate = models.DateTimeField()
        renewaldate = models.DateTimeField(null=True, blank=True)
        reinstateddate = models.DateTimeField(null=True, blank=True)
        cancellationdate = models.DateTimeField(null=True, blank=True)
        statuscode = models.ForeignKey(memberstatus, on_delete=models.DO_NOTHING, to_field='memberstatuscode')
        hib = models.IntegerField()
        covid = models.IntegerField()
        tin = models.CharField(max_length=255)
        address = models.CharField(max_length=255)
        locationcode = models.IntegerField()
        contactnumber = models.CharField(max_length=255)
        emailaddress = models.CharField(max_length=255)
        remarks = models.TextField()
        transactby =  models.IntegerField()
        transactdate = models.DateTimeField()
        transactype = models.CharField(max_length=50)
        class Meta:
            db_table="member"

        # def save(self, *args, **kwargs):
        #         # Generate policy number only if it's not set
        #         if not self.policynumber:
        #             # Use clientcode as coop code
        #             coop_code = self.clientcode[:5].zfill(5)  # Ensure it's exactly 5 characters
        #             # Format date as MMYY from effectivedate
        #             date_part = self.effectivedate.strftime("%m%y")
        #             # Use membercode with zero padding to ensure it is 6 characters
        #             member_code_formatted = str(self.membercode).zfill(6)
        #             # Construct the policy number
        #             self.policynumber = f"{coop_code}-{date_part}-{member_code_formatted}"
                
        #         super(member, self).save(*args, **kwargs)     

class historymember(models.Model):
        recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
        recordno = models.IntegerField()
        membercode = models.CharField(max_length=100)
        policynumber = models.CharField(max_length=255)
        thirdpartyid = models.CharField(max_length=255)
        otherid = models.CharField(max_length=255)
        clientcode = models.ForeignKey(client, on_delete=models.DO_NOTHING, to_field='clientcode')
        branchcode = models.IntegerField()
        membertypecode = models.IntegerField()
        lastname = models.CharField(max_length=255)
        firstname = models.CharField(max_length=255)
        middlename = models.CharField(max_length=255)
        birthdate = models.DateField()
        enrollage = models.DecimalField(max_digits=10, decimal_places=2)
        gendercode = models.ForeignKey(membergender, on_delete=models.DO_NOTHING, to_field='membergendercode')
        civilstatuscode = models.IntegerField()
        effectivedate = models.DateTimeField()
        expirydate = models.DateTimeField()
        renewaldate = models.DateTimeField(null=True, blank=True)
        reinstateddate = models.DateTimeField(null=True, blank=True)
        cancellationdate = models.DateTimeField(null=True, blank=True)
        statuscode = models.ForeignKey(memberstatus, on_delete=models.DO_NOTHING, to_field='memberstatuscode')
        hib = models.IntegerField()
        covid = models.IntegerField()
        tin = models.CharField(max_length=255)
        address = models.CharField(max_length=255)
        locationcode = models.IntegerField()
        contactnumber = models.CharField(max_length=255)
        emailaddress = models.CharField(max_length=255)
        remarks = models.TextField()
        transactby =  models.IntegerField()
        transactdate = models.DateTimeField()
        transactype = models.CharField(max_length=50)
        transactby =  models.IntegerField()
        transactdate = models.DateTimeField()
        transactype = models.CharField(max_length=50)
        class Meta:
            db_table="historymember"
            indexes = [
            models.Index(fields=['recordno'], name='memberh_idx'),
        ]
