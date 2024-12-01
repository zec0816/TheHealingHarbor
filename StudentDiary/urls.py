from django.urls import path
from . import views

app_name = "StudentDiary"

urlpatterns = [
    path('diary',views.diary,name="diary"),
    path('diaryadd/',views.diaryadd,name="diaryadd"),
    path("diaryaddrec/",views.diaryaddrec,name="diaryaddrec"),
    path('diarydelete/<int:id>/',views.diarydelete,name="diarydelete"),
    path('diaryupdate/<int:id>/',views.diaryupdate,name="diaryupdate"),
    path('diaryupdate/uprec/<int:id>/',views.diaryuprec,name="diaryuprec"),
]