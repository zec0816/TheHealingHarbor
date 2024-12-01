from django.shortcuts import render, redirect, get_object_or_404, reverse
from Home.decorators import student_required
from Home.models import Counselor, User
from CounselorSchedule.models import Timeslot
from .models import Appointments
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from datetime import date


# Create your views here.
@student_required
def ExpertView(request): 
    query = request.GET.get('query')        #get query from GET request (search bar functionality)
    counselors = Counselor.objects.exclude(qualification="", self_description="").exclude(schedule__isnull=True)    #first exclude counselor with no qualification field and no self description field, also exclude counselor with no schedule
    counselors_to_exclude = []

    for counselor in counselors:
      timeslots = counselor.schedule.all()         #storing in a list
      if all(timeslot.date < date.today() for timeslot in timeslots):
        counselors_to_exclude.append(counselor)             #check whether all timeslots are in the past
      else:
        future_timeslots = [timeslot for timeslot in timeslots if timeslot.date >= date.today()] 
        if all(timeslot.is_booked for timeslot in future_timeslots): #check whether all future timeslots are booked
            counselors_to_exclude.append(counselor)

    counselors = counselors.exclude(pk__in=[counselor.pk for counselor in counselors_to_exclude]) #exclude counselors that are already booked based on their primary key in list
    
    #search function 
    if query and query != " ":
        counselors = counselors.filter(full_name__icontains=query)       #search if counselor's name contains query

    return render(request, 'expert.html', {'counselors': counselors, 'query': query})

@method_decorator(student_required, name='dispatch')
class AppointmentView(View): 
    model = Timeslot
    template_name = 'appointment.html'
    context_object_name = 'counselor'

    def get(self, request, *args, **kwargs):
        student_name = request.user.student.full_name            #get name of student logged in and counselor name that student selected
        try:
            counselor = Counselor.objects.get(pk=self.kwargs['pk'])
            counselor_id = self.kwargs['pk']
        except Counselor.DoesNotExist:
            message = f"The counselor does not exist. Please refer here..."
            messages.error(request, message)
            return redirect('/student/experts/')
        
        # Check if counselor info is filled in (for the case if someone search counselor that does not fill in their details by url directly)
        if counselor.qualification == "" or counselor.self_description == "":
            message = f"The counselor is currently unavailable. Kindly choose for other..."
            messages.error(request, message)
            return redirect('/student/experts/')
        
        timeslots = counselor.schedule.all()
        if not timeslots or all(timeslot.date <= date.today() for timeslot in timeslots) or all(timeslot.is_booked for timeslot in timeslots):
          message = "No timeslots available for this counselor."
          messages.error(request, message)
          return redirect('/student/experts/')
        
            
        available_slots = []
        today = date.today()
        for timeslot in timeslots:
          if not timeslot.is_booked and timeslot.date >= today:            #get the available timeslots that are not booked and are in the future
            available_slots.append({
            'date': timeslot.date.strftime('%Y-%m-%d'),    
            'start': timeslot.start.strftime('%H:%M:%S'),
            'end': timeslot.end.strftime('%H:%M:%S')
          })
    
        return render(request, self.template_name, {'counselor': counselor, 'student_name': student_name, 'available_slots':available_slots})

    def post(self, request, *args, **kwargs):
        # Get data from the form
        appointment_name = request.POST['appointmentTitle']
        appointment_date = request.POST['dropdowndates']
        appointment_time = request.POST['time']
        appointment_desc = request.POST['appointmentdesc']

        start_time, end_time = appointment_time.split(' - ')

        # Get the counselor object
        try:
            counselor = Counselor.objects.get(pk=self.kwargs['pk'])
        except Counselor.DoesNotExist:
            message = f"The counselor does not exist. Please refer here.."
            messages.error(request, message)
            return redirect('/student/experts/')

        # Check if counselor info is filled in
        if counselor.qualification == "" or counselor.self_description == "":
            message = f"The counselor is currently unavailable. Kindly choose for other..."
            messages.error(request, message)
            return redirect('/student/experts/')

        # Get the timeslot object
        try:
            timeslot = Timeslot.objects.get(date=appointment_date, start=start_time, end=end_time)
        except Timeslot.DoesNotExist:
            message = f"The selected timeslot is not available. Please select another..."
            messages.error(request, message)
            return redirect('/student/experts/')

        # Create a new appointment object and save it to the database
        appointment = Appointments.objects.create(
            student=request.user.student,
            counselor=counselor,
            timeslot=timeslot,
            title=appointment_name,
            description=appointment_desc,
            created_at=timezone.now()
        )

        # Mark the corresponding timeslot as booked
        timeslot.is_booked = True
        timeslot.save()

        message = f"Booked successfully!"
        messages.success(request, message)
        return redirect('/student/appointment/')

@student_required
def MyAppointmentView(request): 
    message = None
    student_name = request.user.student.full_name
    appointment = Appointments.objects.filter(student__full_name=student_name, timeslot__date__gte=date.today())       #only show upcoming appointments that are in the future
    if len(appointment) == 0:
        message = f"No upcoming appointments so far. Get one now!"
    print(appointment)
    return render(request, 'myappointment.html', {'appointment': appointment, 'message': message})

@student_required
def DeleteAppointmentView(request, pk):
    try:
      appointment = Appointments.objects.get(pk=pk)          #delete the appointment
      appointment.timeslot.is_booked = False
      appointment.delete()
      message = f"Deleted successfully!"
      messages.success(request, message, extra_tags='success')
    except Appointments.DoesNotExist:
      message = f"The appointment does not exist..."
      messages.error(request, message, extra_tags='error')
    return redirect('/student/appointment/')

