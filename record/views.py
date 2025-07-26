from django.shortcuts import render
from core.ui import default_dict
from core.models import fetch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required
def select_factory(request):
    return render(request,"select_factory.html",default_dict(request))
@require_http_methods(["GET"])
@login_required
def index(request,type,id):
    return render(request,"index.html",default_dict(request,{"type":type,"id":id,"object":fetch(type,id)}))