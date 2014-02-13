from django.db import models

# Create your models here.
class MainInfo(models.Model):
    vendor = models.CharField(max_length = 30)
    product = models.CharField(max_length = 30)
    hver = models.CharField(max_length = 10)
    batch = models.IntegerField()
    mac = models.IntegerField()

class MainInfoSn(models.Model):
    device = models.CharField(max_length = 30)
    number = models.IntegerField()
    
class SavedMainInfo(models.Model):
    vendor = models.CharField(max_length = 30)
    product = models.CharField(max_length = 30)
    sn   = models.CharField(max_length = 20)
    hver = models.CharField(max_length = 10)
    pdate = models.CharField(max_length = 30)
    mac = models.CharField(max_length = 30)
    batch = models.CharField(max_length = 10)

class SavedExternInfo(models.Model):
    vendor = models.CharField(max_length = 30)
    product = models.CharField(max_length = 30)
    sn   = models.CharField(max_length = 20)
    hver = models.CharField(max_length = 10)
    pdate = models.CharField(max_length = 30)
    batch = models.CharField(max_length = 10)

    
