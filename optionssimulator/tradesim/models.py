from django.db import models


class displaydata(models.Model):
    name= models.CharField(max_length=20)
    value=models.FloatField(max_length=10)
    percentagechange=models.FloatField(max_length=5)

class positions(models.Model):
    token=models.IntegerField()
    strategy= models.CharField(max_length=100)
    createdon= models.DateTimeField()
    bs= models.CharField(max_length=1)
    expiry=models.CharField(max_length=10)
    strike= models.FloatField(max_length=10)
    cepe= models.CharField(max_length=2)
    lots= models.IntegerField()
    entry= models.FloatField(max_length=10)
    stoploss= models.FloatField(max_length=10, null=True)
    price= models.FloatField(max_length=10, null=True)
    pnl= models.FloatField(max_length=10,default=0.0, null=True)
    active=models.BooleanField(default=True)
    archived=models.BooleanField(default=False)

class optionchain(models.Model):
    ctoken=models.IntegerField()
    ptoken=models.IntegerField()
    expiry=models.CharField(max_length=10)
    strike= models.FloatField(max_length=10)
    cltp= models.FloatField(max_length=100)
    coi= models.FloatField(max_length=100)
    pltp= models.FloatField(max_length=100)
    poi= models.FloatField(max_length=100)

class inview(models.Model):
    strategy= models.CharField(max_length=100)
    createdon= models.DateTimeField()
    expiry=models.CharField(max_length=10)

class builder(models.Model):
    token=models.IntegerField()
    strategy= models.CharField(max_length=100, null=True)
    createdon= models.DateTimeField(null=True)
    bs= models.CharField(max_length=1)
    expiry=models.CharField(max_length=10, null=True)
    strike= models.FloatField(max_length=10, null=True)
    cepe= models.CharField(max_length=2, null=True)
    lots= models.IntegerField(default=1, null=True)
    price= models.FloatField(max_length=10, null=True)

class dashboard(models.Model):
    strategy= models.CharField(max_length=100)
    createdon= models.DateTimeField()
    maxprofit =models.FloatField(max_length=100)
    maxloss= models.FloatField(max_length=100)
    rrr= models.FloatField(max_length=10)
    breakeven1= models.FloatField(max_length=100)
    breakeven2= models.FloatField(max_length=100)
    projectedreturns= models.FloatField(max_length=10)
    marginavailable = models.FloatField(max_length=100)
    marginneeded = models.FloatField(max_length=100)
    marginused = models.FloatField(max_length=100)




