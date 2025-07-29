from django.shortcuts import render,redirect
from core.ui import default_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,login,logout

@require_http_methods(["GET","POST"])
def loginview(request):
    if request.method == "GET":
        return render(request,"login.html",default_dict(request))
    else:
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if not username or not password:
            messages.error(request,"用户名密码都不能为空")
            return redirect("")
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            request.session["firstvisit"] = True
            return redirect("/" if not request.GET.get("next") else request.GET.get("next"))
        else:
            messages.error(request,"用户名或密码错误")
            return redirect("")
@require_http_methods(["GET"])
@login_required
def logoutview(request):
    logout(request)
    return redirect("/")