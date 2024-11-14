from django.db import models

# Create your models here.
class Sob(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    sobcode = models.IntegerField(unique=True)
    sobname = models.CharField(max_length=255, blank=False)
    sobshortname = models.CharField(max_length=50, null=True)
    remarks = models.TextField(null=True)
    transactby = models.IntegerField()
    transactdate = models.DateTimeField()
    transacttype = models.CharField(max_length=10)
    class Meta:
        db_table="Sob"
        indexes = [
            models.Index(fields=['sobcode'], name='sobcode_idx'),
            models.Index(fields=['sobcode', 'sobname'], name='sobcode_sobname_idx'),
        ]

class SobHistory(models.Model):
    recordnohist = models.BigAutoField(auto_created=True, primary_key=True)
    recordno = models.IntegerField()
    sobcode = models.IntegerField()
    sobname = models.CharField(max_length=255, blank=False)
    sobshortname = models.CharField(max_length=50, null=True)
    remarks = models.TextField(null=True)
    transactby = models.IntegerField()
    transactdate = models.DateTimeField()
    transacttype = models.CharField(max_length=10)
    class Meta:
        db_table="SobHistory"
        indexes = [
            models.Index(fields=['recordno'], name='sobrecordnoh_idx'),
            models.Index(fields=['sobcode'], name='sobcodeh_idx'),
            models.Index(fields=['sobcode', 'sobname'], name='sobcode_sobnameh_idx'),
        ]