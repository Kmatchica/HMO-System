from django.db import models
from category_app.models import category
from providerstatus_app.models import providerstatus
# Create your models here.
class provider(models.Model):
     recordno = models.BigAutoField(auto_created=True, primary_key=True)
     providercode = models.IntegerField(unique=True)
     categorycode = models.ForeignKey(category, on_delete=models.DO_NOTHING, to_field='categorycode')
     providername = models.CharField(max_length=100)
     tin = models.CharField(max_length=100)
     address = models.CharField(max_length=100)
     locationcode = models.IntegerField(unique=True)
     emailaddress = models.CharField(max_length=100)
     contactperson = models.CharField(max_length=100)
     landline = models.CharField(max_length=100)
     mobilenumber = models.CharField(max_length=100)
     providerstatuscode = models.ForeignKey(providerstatus, on_delete=models.DO_NOTHING, to_field='providerstatuscode')
     accreditdate = models.DateField(null=True, blank=True)
     suspensiondate = models.DateField(null=True, blank=True)
     disaccreditdate = models.DateField(null=True, blank=True)
     reaccreditdate = models.DateField(null=True, blank=True)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="provider"#new userdatabase
         indexes = [
            models.Index(fields=['locationcode'], name='locationcode_idx'),
            models.Index(fields=['locationcode', 'address'], name='address'),
        ]
         
class historyprovider(models.Model):
     recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
     recordno = models.IntegerField()
     providercode =  models.IntegerField()
     categorycode = models.ForeignKey(category, on_delete=models.DO_NOTHING, to_field='categorycode')
     providername = models.CharField(max_length=100)
     tin = models.CharField(max_length=100)
     address = models.CharField(max_length=100, blank=False)
     locationcode= models.IntegerField()
     emailaddress = models.CharField(max_length=100)
     contactperson = models.CharField(max_length=100)
     landline =  models.CharField(max_length=100)
     mobilenumber = models.CharField(max_length=100)
     providerstatuscode = models.ForeignKey(providerstatus, on_delete=models.DO_NOTHING, to_field='providerstatuscode')
     accreditdate = models.DateField(null=True, blank=True)
     suspensiondate = models.DateField(null=True, blank=True)
     disaccreditdate = models.DateField(null=True, blank=True)
     reaccreditdate = models.DateField(null=True, blank=True)
     remarks = models.CharField(max_length=100)
     status = models.CharField(max_length=100)
     transactby =  models.IntegerField()
     transactdate = models.DateTimeField()
     transactype = models.CharField(max_length=50)
     class Meta:
         db_table="historyprovider"#new userdatabase
         indexes = [
            models.Index(fields=['recordno'], name='providerrecordh_idx'),
            models.Index(fields=['locationcode'], name='locationcodeh_idx'),
            models.Index(fields=['locationcode', 'address'], name='addressh'),
        ]         
