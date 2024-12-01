from django.shortcuts import redirect, render
from .models import Timeslot
from datetime import datetime, date
from Home.decorators import counselor_required
from django.core.exceptions import ValidationError

# Create your views here.
@counselor_required
def index(request):           #displaying timeslot for counselor that is logged in at the time
    slots = Timeslot.objects.filter(counselor=request.user.counselor)
    return render(request, 'index.html', {'slot': slots})

@counselor_required
def add(request):
    today_date = date.today().strftime('%Y-%m-%d')
    error = request.session.pop('add_error', None)  # Retrieve the error message from the session
    return render(request, 'add.html', {'today_date': today_date, 'error': error})

@counselor_required
def addrec(request):                     #create timeslots for counselor
    date_str = request.POST['date']
    start_str = request.POST['start']
    end_str = request.POST['end']
    counselor = request.user.counselor

    try:
        current_date = date.today()
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_str, '%H:%M').time()            #getting the current date and time
        end_time = datetime.strptime(end_str, '%H:%M').time()

        current_datetime = datetime.combine(current_date, datetime.now().time())

        if selected_date == current_date and start_time < current_datetime.time():
            raise ValidationError('Start time cannot be in the past')                         #validation to make sure date is not in the past

        if selected_date < current_date:
            raise ValidationError('Selected date cannot be in the past')

        if start_time >= end_time:
            raise ValidationError('Start time should be earlier than end time')

        day = selected_date.strftime('%A')

        slot = Timeslot(counselor=counselor, date=selected_date, day=day, start=start_time, end=end_time)
        slot.full_clean()  # Validate the model instance
        slot.save()
        return redirect("CounselorSchedule:index")

    except (ValueError, ValidationError) as e:
        request.session['add_error'] = str(e)  # Store the error message in the session
        return redirect("CounselorSchedule:add")

@counselor_required
def delete(request, id):
    slot = Timeslot.objects.get(id=id)        #get the id of the timeslot that is to be deleted
    slot.delete()
    return redirect("CounselorSchedule:index")
    
@counselor_required
def update(request, id):
    slot = Timeslot.objects.get(id=id)
    today_date = date.today().strftime('%Y-%m-%d')
    error = request.session.pop('update_error', None)  # Retrieve the error message from the session
    return render(request, 'update.html', {'slot': slot, 'today_date': today_date, 'error': error})

@counselor_required
def uprec(request, id):
    slot = Timeslot.objects.get(id=id)
    date_str = request.POST['date']
    start_str = request.POST['start']
    end_str = request.POST['end']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_time = datetime.strptime(start_str, '%H:%M').time()
    end_time = datetime.strptime(end_str, '%H:%M').time()

    try:
        current_date = date.today()
        current_datetime = datetime.combine(current_date, datetime.now().time())

        if date == current_date and start_time < current_datetime.time():
            raise ValidationError('Start time cannot be in the past')

        if date < current_date:
            raise ValidationError('Selected date cannot be in the past')

        if start_time >= end_time:
            raise ValidationError('Start time should be earlier than end time')

        day = date.strftime('%A')

        slot.date = date
        slot.day = day             #updating the timeslot
        slot.start = start_time
        slot.end = end_time
        slot.full_clean()  # Validate the model instance
        slot.save()
        return redirect("CounselorSchedule:index")

    except (ValueError, ValidationError) as e:
        request.session['update_error'] = str(e)  # Store the error message in the session
        return redirect("CounselorSchedule:update", id=id)