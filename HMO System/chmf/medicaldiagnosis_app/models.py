from django.db import models

class diagnosis(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    diagnosiscode = models.IntegerField(unique=True)
    diagnosisname = models.CharField(max_length=100)
    diagnosisshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="diagnosis"

class historydiagnosis(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    diagnosiscode = models.IntegerField()
    diagnosisname = models.CharField(max_length=100)
    diagnosisshortname = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    transactby =  models.IntegerField()
    transactdate = models.DateTimeField()
    transactype = models.CharField(max_length=50)
    class Meta:
        db_table="historydiagnosis"
        indexes = [
        models.Index(fields=['recordno'], name='diagnosish_idx'),
    ]
    