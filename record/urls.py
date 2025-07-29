from django.urls import path,re_path
from . import views
urlpatterns = [
    path("",views.select_factory),
    path("<type>/<int:id>/",views.index),
    path("<int:id>/edit/",views.edit),
    path("add/",views.edit),
    path("export/<type>/<int:id>/",views.export),
]