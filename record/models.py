from django.db import models
from django.contrib.auth.models import User
from core.models import Machine
from datetime import datetime
import json
# Create your models here.
class Record(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,models.PROTECT,null=False)
    title = models.CharField(max_length=256,null=False)
    errcode = models.CharField(max_length=256,null=True,blank=True)
    detail = models.TextField(null=False)
    solution = models.TextField(null=False)
    attachments = models.TextField(null=False,default="[]")
    machine = models.ForeignKey(Machine,models.CASCADE,null=False)
    created_time = models.DateTimeField(null=False,default=datetime.now)
    def __str__(self):
        return "<Record %s->%s for %s on %s>"%(self.title,self.errcode,self.machine.name,self.created_time.strftime("%Y/%m/%d %H:%M"))
    def tojson(self):
        return {"id":self.id,
                "user":self.user.username,
                "title":self.title,
                "errcode":self.errcode,
                "detail":self.detail,
                "solution":self.solution,
                "attachments":json.loads(self.attachments),
                "machine":self.machine.name,
                "pipeline":self.machine.pipeline.index,
                "garage":self.machine.pipeline.garage.index,
                "factory":self.machine.pipeline.garage.factory.index,
                "created_time":self.created_time.strftime("%Y/%m/%d %H:%M")}