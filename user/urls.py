from django.urls import path,re_path
from . import views
urlpatterns = [
    path("login/",views.loginview),
    path("logout/",views.logoutview)
]