from django.urls import path
from . import views

app_name = "StudentAppointment"

urlpatterns = [
    path('experts/', views.ExpertView, name="experts"),
    path('expert/<int:pk>/', views.AppointmentView.as_view(), name='appointment'),
    path('appointment/', views.MyAppointmentView, name="myAppointment"),
    path('appointment/delete/<int:pk>/', views.DeleteAppointmentView, name="deleteAppointment"),
]
