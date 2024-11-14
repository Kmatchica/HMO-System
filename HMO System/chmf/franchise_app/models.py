from django.db import models

from MeansofFranchise_app.models import MeansofFranchise
from Franchisestatus_app.models import Franchisestatus

class franchise(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    franchisecode= models.IntegerField()
    clientname= models.CharField(max_length=200)
    clientshortname= models.CharField(max_length=200)
    clientclassificationcode = models.IntegerField()
    address = models.CharField(max_length=200)
    contactnumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contactperson = models.CharField(max_length=200)
    contactpersondesignation = models.CharField(max_length=200)
    signatoryname = models.CharField(max_length=200)
    signatorydesignation = models.CharField(max_length=200)
    totalmembers = models.IntegerField()
    totaldependents = models.IntegerField()
    totalemployees = models.IntegerField()
    existinghmo = models.CharField(max_length=200)
    sobtypeid = models.IntegerField()
    meansofknowingid= models.ForeignKey(MeansofFranchise, on_delete=models.DO_NOTHING, to_field='meansofknowingid', blank=True)
    referredby = models.CharField(max_length=200)
    franchisestatusid= models.ForeignKey(Franchisestatus, on_delete=models.DO_NOTHING, to_field='franchisestatusid', blank=True)
    disapprovalreason = models.CharField(max_length=200)
    istpa = models.CharField(max_length=200)
    adminfee = models.CharField(max_length=200)
    networkaccessfee = models.CharField(max_length=200)
    locationcode = models.IntegerField()
    remarks = models.CharField(max_length=200)
    status= models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="franchise"


class historyfranchise(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    franchisecode= models.IntegerField()
    clientname= models.CharField(max_length=200)
    clientshortname= models.CharField(max_length=200)
    clientclassificationcode = models.IntegerField()
    address = models.CharField(max_length=200)
    contactnumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contactperson = models.CharField(max_length=200)
    contactpersondesignation = models.CharField(max_length=200)
    signatoryname = models.CharField(max_length=200)
    signatorydesignation = models.CharField(max_length=200)
    totalmembers = models.IntegerField()
    totaldependents = models.IntegerField()
    totalemployees = models.IntegerField()
    existinghmo = models.CharField(max_length=200)
    sobtypeid = models.IntegerField()
    meansofknowingid= models.ForeignKey(MeansofFranchise, on_delete=models.DO_NOTHING, to_field='meansofknowingid', blank=True)
    referredby = models.CharField(max_length=200)
    franchisestatusid= models.ForeignKey(Franchisestatus, on_delete=models.DO_NOTHING, to_field='franchisestatusid', blank=True)
    disapprovalreason = models.CharField(max_length=200)
    istpa = models.CharField(max_length=200)
    adminfee = models.CharField(max_length=200)
    networkaccessfee = models.CharField(max_length=200)
    locationcode = models.IntegerField()
    remarks = models.CharField(max_length=200)
    status= models.CharField(max_length=200)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historyfranchise"
        indexes = [
            models.Index(fields=['recordno'], name='franchiserecordh_idx'),
            
        ]

