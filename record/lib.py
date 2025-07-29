from datetime import datetime,timedelta
from django.db.models import Q
def search_filter(query,keyword=None,machine_name=None,start_time=None,end_time=None):
    if keyword:
        query = query.filter(Q(errcode=keyword)|Q(title__contains=keyword))
    if machine_name:
        query = query.filter(machine__name=machine_name)
    if start_time:
        start_time = datetime.strptime(start_time,"%Y-%m-%d")
        query = query.filter(created_time__gte=start_time)
    if end_time:
        end_time = datetime.strptime(end_time,"%Y-%m-%d") + timedelta(days=1)
        query = query.filter(created_time__lt=end_time)
    return query
def place_filter(query,type,dbobject):
    if type == "pipeline":
        query = query.filter(machine__pipeline=dbobject)
    elif type == "garage":
        query = query.filter(machine__pipeline__garage=dbobject)
    else:
        query = query.filter(machine__pipeline__garage__factory=dbobject)
    return query