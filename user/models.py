from django.db import models
from django.contrib.auth.models import User
from core.models import Factory,Garage,Pipeline,Machine
from core.constants import *

class Access(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,models.CASCADE,null=False)
    factory = models.ForeignKey(Factory,models.CASCADE,null=True,blank=True)
    garage = models.ForeignKey(Garage,models.CASCADE,null=True,blank=True)
    pipeline = models.ForeignKey(Pipeline,models.CASCADE,null=True,blank=True)
    access = models.IntegerField(null=False,default=0)
    def __str__(self):
        if self.pipeline:
            r = "p-%s"%self.pipeline.index
        elif self.garage:
            r = "g-%s"%self.garage.index
        elif self.factory:
            r = "f-%s"%self.factory.index
        t = ""
        for i in ACCESS:
            if self.access & ACCESS[i]:
                t += list(i)[0]
            else:
                t += "-"
        return "<Access %s@%s:%s>"%(self.user.username,r,t)
def check_access(user:User,pipeline=None,garage=None,factory=None):
    if user.is_superuser:
        return MAX_ACCESS
    access = user.access_set
    if pipeline:
        r = access.filter(pipeline=pipeline).first()
        if r:
            return r.access
        else:
            garage = pipeline.garage
    if garage:
        r = access.filter(garage=garage).first()
        if r:
            return r.access
        else:
            factory = garage.factory
    if factory:
        r = access.filter(factory=factory).first()
        if r:
            return r.access
    return 0