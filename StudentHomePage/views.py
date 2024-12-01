from django.shortcuts import render, redirect
from Home.decorators import student_required
from Counselorinfosection.models import Info
from Home.models import User, Student
from django.contrib import messages
# Create your views here.

@student_required
def IndexView(request): 
    user = request.user
    message = None
    try:
        student = user.student

    except Student.DoesNotExist:       #check if the user is a student
        message = 'Your account does not exist, it may have been deleted.'
        messages.error(request, message)              
        return redirect('login/')
    
    if not student.full_name or not student.phone_number:
        message = 'Please complete your profile information.'
        print(message)
   
    info = Info.objects.all().order_by('-id')       #get all infos that are published based on the info section order by id
    return render(request, 'studentHomePage.html', {'info': info, 'message':message})
