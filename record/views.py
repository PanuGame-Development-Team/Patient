from django.shortcuts import render,redirect
from core.ui import default_dict
from core.models import fetch,Factory,Pipeline,Machine
from core.constants import *
from Patient.settings import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Record
from user.models import check_access
from uuid import uuid4
from json import dumps,loads
from markdown import markdown
from csv import DictWriter
from .lib import *

@require_http_methods(["GET"])
@login_required
def select_factory(request):
    return render(request,"select_factory.html",default_dict(request,{"factories":Factory.objects.all()}))
@require_http_methods(["GET"])
@login_required
def index(request,type,id):
    from datetime import datetime
    object = fetch(type,id)
    access = check_access(request.user,**{type:object})
    writable = access&ACCESS["WRITE"]
    exportable = access&ACCESS["EXPORT"]
    return render(request,"index.html",default_dict(request,{"type":type,"id":id,"object":object,"writable":writable,"exportable":exportable}))
@require_http_methods(["GET","POST"])
@login_required
def edit(request,id=None):
    if id:
        object = Record.objects.filter(id=id).first()
        pipeline = object.machine.pipeline
    else:
        object = Record()
        object.user = request.user
        pipeline = Pipeline.objects.filter(id=int(request.GET.get("id"))).first()
        machines = pipeline.machine_set.all()
    if not check_access(request.user,pipeline)|ACCESS["WRITE"] or not request.user == object.user or not object:
        messages.warning(request,"你没有修改此条记录的权限")
        return redirect("/")
    if request.method == "GET":
        if id:
            return render(request,"edit.html",default_dict(request,{"object":object,"operation":"modify"}))
        else:
            return render(request,"edit.html",default_dict(request,{"object":object,"operation":"add","machines":machines}))
    else:
        files = request.FILES.getlist("attachments")
        filelist = []
        for i in files:
            filename = uuid4().hex + "." + i.name.split(".")[-1]
            with open(STATIC_ROOT + "/uploads/" + filename,"wb") as file:
                for chunk in i.chunks():
                    file.write(chunk)
            filelist.append("/static/uploads/" + filename)
        if files:
            object.attachments = dumps(filelist)
        object.title = request.POST.get("title","")
        object.errcode = request.POST.get("errcode","")
        object.detail = markdown(request.POST.get("detail",""))
        object.solution = markdown(request.POST.get("solution",""))
        if not id:
            try:
                object.machine = Machine.objects.filter(id=int(request.POST.get("machine",""))).first()
            except:
                messages.warning(request,"请输入合理的结果")
                return redirect(f"/record/pipeline/{pipeline.id}/")
        object.save()
        messages.success(request,"修改成功" if id else "添加成功")
        return redirect(f"/record/pipeline/{pipeline.id}/")
@require_http_methods(["GET"])
@login_required
def export(request,type,id):
    filename = uuid4().hex + ".csv"
    with open(STATIC_ROOT + "/exports/" + filename,"w",encoding="UTF-8") as file:
        headers = ["id","user","title","errcode","detail","solution","machine","pipeline",
                   "garage","factory","created_time"]
        writer = DictWriter(file,headers,extrasaction="ignore")
        writer.writeheader()
        query = place_filter(Record.objects,type,fetch(type,id))
        filter = loads(request.GET.get("filter",'["","","",""]'))
        query = search_filter(query,*filter)
        objects = query.all()
        for i in objects:
            writer.writerow(i.tojson())
    return redirect("/static/exports/" + filename)