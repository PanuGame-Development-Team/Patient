from django.urls import path,re_path
from . import views
urlpatterns = [
    path("",views.select_factory),
    path("<type>/<int:id>/",views.index)
]