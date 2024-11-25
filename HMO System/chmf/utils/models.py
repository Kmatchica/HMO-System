from django.db import models
from django.utils.timezone import now

class CodeCounter(models.Model):
    recordno = models.BigAutoField(auto_created=True, primary_key=True)
    countername = models.CharField(max_length=100)  
    counterresetbasis = models.CharField(max_length=50, default="Year")  # Reset basis (e.g., 'Year', 'Month')
    counter = models.IntegerField(default=0)  
    transactdate = models.DateTimeField(auto_now=True)  
    class Meta:
        db_table="CodeCounter"
