from django.urls import path
from . import views

app_name = "infosection"

urlpatterns = [
    path('',views.info,name="info"),
    path('infoadd/',views.infoadd,name="infoadd"),
    path("infoaddrec/",views.infoaddrec,name="infoaddrec"),
    path('infodelete/<int:id>/',views.infodelete,name="infodelete"),
    path('infoupdate/<int:id>/',views.infoupdate,name="infoupdate"),
    path('infoupdate/uprec/<int:id>/',views.infouprec,name="infouprec"),
]