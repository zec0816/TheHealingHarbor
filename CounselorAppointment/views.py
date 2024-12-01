from django.shortcuts import render, redirect
from StudentAppointment.models import Appointments
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def counselor_appointments(request):
    counselor = request.user.counselor  # Assuming the logged-in user is a counselor
    appointments = Appointments.objects.filter(counselor=counselor) #filter the appointments based on the counselor
    context = {
        'appointments': appointments,
    }
    return render(request, 'counselorappointment.html', context)

@login_required
def appointment_delete(request, id):
    try:
      booked = Appointments.objects.get(id=id) #get appointment with the id
      booked.delete()
    except Appointments.DoesNotExist:
      message = f"The appointment does not exist..."
      messages.error(request, message, extra_tags='error')
    return redirect("CounselorAppointment:counselor_appointments")
