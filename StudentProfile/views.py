from django.shortcuts import render, redirect, reverse
from Home.models import Student
from django.utils import timezone
from .forms import UpdateUserForm, UpdateStudentForm
from Home.decorators import student_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
        
@student_required
def ProfileView(request): 
   try:
        profile = Student.objects.filter(user=request.user).first()
        if profile and profile.student_profile:
          has_profile_picture = True
          
          if os.path.exists(os.path.join(settings.MEDIA_ROOT, profile.student_profile.name)):          #check if the file exists in media directory
            profile_picture_url = profile.student_profile.url
          else:
            profile_picture_url = settings.MEDIA_URL + 'default.png'       #return default.png's url if file does not exist
        else:
          has_profile_picture = False
          profile_picture_url = settings.MEDIA_URL + 'default.png'
   except Student.DoesNotExist:
        message = "Please login / create an account first"
        messages.error(request, message)
        return redirect(reverse('Home:login'))
  
   return render(request, 'studentprofile.html', {'profile': profile, 'profile_picture_url': profile_picture_url})


@student_required
def EditProfileView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
          user_form = UpdateUserForm(request.POST or None, instance=request.user)
          student_form = UpdateStudentForm(request.POST or None, request.FILES, instance=request.user.student)

          if user_form.has_changed() or student_form.has_changed():     #check whether there are any changes
            if user_form.is_valid() and student_form.is_valid():
              new_profile_picture = student_form.cleaned_data.get('student_profile')
              user = user_form.save(commit=False)
              student = student_form.save(commit=False)

              if new_profile_picture and new_profile_picture != student.student_profile:    #if profile picture is changed and it is not the same
               old_profile_picture = Student.objects.get(user=request.user).student_profile
               if old_profile_picture.name != 'default.png':
                 old_profile_picture_path = old_profile_picture.path
                 if default_storage.exists(old_profile_picture_path):    #delete old profile picture
                   default_storage.delete(old_profile_picture_path)   

              student.student_profile = new_profile_picture

            else:
               messages.error(request, 'There was an error updating your profile.')
               return redirect(reverse('StudentProfile:studentprofile'))
            
            user_form.save()
            student_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(reverse('StudentProfile:studentprofile'))
          
          else:
            messages.info(request, 'No changes were made to your profile.')
            return redirect(reverse('StudentProfile:studentprofile'))
          
        else:
          user_form = UpdateUserForm(instance=request.user)
          student_form = UpdateStudentForm(instance=request.user.student)

          return render(request, 'editstudentprofile.html', {'user_form': user_form, 'student_form': student_form})

    else:
       message = 'You must be logged in to view this!'
       messages.error(request, message)
       return redirect(reverse('Home:login'))


class StudentChangePasswordView(SuccessMessageMixin, PasswordChangeView):        #built-in Django view
   template_name = 'changestudentpassword.html'    
   success_url = reverse_lazy('StudentProfile:studentprofile')       # url to redirect to after successful password change
   success_message = "Password successfully changed."

   def form_valid(self, form):
        response = super().form_valid(form)
        return response