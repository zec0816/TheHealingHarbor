from django.urls import path
from .views import counselor_appointments, appointment_delete

app_name = "CounselorAppointment"

urlpatterns = [
    path('appointments/', counselor_appointments, name='counselor_appointments'),
    path('appointment_delete/<int:id>/', appointment_delete, name="appointment_delete"),
]
