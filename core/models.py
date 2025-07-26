from django.db import models

# Create your models here.
class Factory(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.CharField(max_length=64,unique=True,null=False)
    def __str__(self):
        return "<Factory %s>"%(self.index)
class Garage(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.CharField(max_length=64,null=False)
    factory = models.ForeignKey(Factory,models.CASCADE)
    def __str__(self):
        return "<Garage %s->%s>"%(self.index,self.factory.index)
class Pipeline(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.CharField(max_length=64,null=False)
    garage = models.ForeignKey(Garage,models.CASCADE)
    def __str__(self):
        return "<Pipeline %s->%s->%s>"%(self.index,self.garage.index,self.garage.factory.index)
class Machine(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.CharField(max_length=64,null=False,unique=True)
    pipeline = models.ForeignKey(Pipeline,models.CASCADE)
    serialnumber = models.CharField(max_length=64,null=False)
    name = models.CharField(max_length=64,null=True,blank=True)
    def __str__(self):
        return "<Machine SN:%s NAME:%s %s->%s->%s->%s>"%(self.serialnumber,self.name,self.index,self.pipeline.index,self.pipeline.garage.index,self.pipeline.garage.factory.index)
def fetch(type,id):
    if type == "factory":
        return Factory.objects.filter(id=id).first()
    elif type == "garage":
        return Garage.objects.filter(id=id).first()
    else:
        return Pipeline.objects.filter(id=id).first()