from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from core.ui import default_dict
@require_http_methods(["GET"])
@login_required
def aichat(request):
    return render(request,"chat.html",default_dict(request))