from django.shortcuts import render, redirect, reverse
from Home.models import Counselor
from .forms import UpdateUserForm, UpdateCounselorForm
from Home.decorators import counselor_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.core.files.storage import default_storage
import os
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
        
@counselor_required
def ProfileView(request): 
   """
   If the user is not logged in or does not have a counselor profile, it redirects to the login page.
   If there is a profile picture, it returns the URL. Otherwise, it returns the default picture URL.
  """
   try:
     profile = Counselor.objects.filter(user=request.user).first()
     if profile and profile.counselor_profile:
       has_profile_picture = True
       # check if the file exists in the media directory
       if os.path.exists(os.path.join(settings.MEDIA_ROOT, profile.counselor_profile.name)):   #check if the file exists in media directory
          profile_picture_url = profile.counselor_profile.url
       else:
            profile_picture_url = settings.MEDIA_URL + 'default.png'   #return default.png's url if file does not exist
     else:
          has_profile_picture = False
          profile_picture_url = settings.MEDIA_URL + 'default.png'
   except Counselor.DoesNotExist:
        message = "Please login / create an account first"
        messages.error(request, message)
        return redirect(reverse('Home:login'))
  
   return render(request, 'counselorprofile.html', {'profile': profile, 'profile_picture_url': profile_picture_url})

@counselor_required
def EditProfileView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
          user_form = UpdateUserForm(request.POST or None, instance=request.user)
          counselor_form = UpdateCounselorForm(request.POST or None, request.FILES, instance=request.user.counselor)

          if user_form.has_changed() or counselor_form.has_changed():    #check whether there are any changes
            if user_form.is_valid() and counselor_form.is_valid():
              new_profile_picture = counselor_form.cleaned_data.get('counselor_profile')   #get profile picture from form
              user = user_form.save(commit=False)
              counselor = counselor_form.save(commit=False)

              if new_profile_picture and new_profile_picture != counselor.counselor_profile:   #if profile picture is changed and it is not the same
                old_profile_picture = Counselor.objects.get(user=request.user).counselor_profile
                if old_profile_picture.name != 'default.png':
                  old_profile_picture_path = old_profile_picture.path   #get the path of profile picture stored in media directory
                  if default_storage.exists(old_profile_picture_path):
                    default_storage.delete(old_profile_picture_path)   #delete old profile picture

              counselor.counselor_profile = new_profile_picture   #set new profile picture

            else:
               messages.error(request, 'There was an error updating your profile.')
               return redirect(reverse('CounselorProfile:counselorprofile'))  

            user_form.save()
            counselor_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(reverse('CounselorProfile:counselorprofile'))
          
          else:
            messages.info(request, 'No changes were made to your profile.')
            return redirect(reverse('CounselorProfile:counselorprofile'))
          
        else:
          user_form = UpdateUserForm(instance=request.user) 
          counselor_form = UpdateCounselorForm(instance=request.user.counselor)
          return render(request, 'editcounselorprofile.html', {'user_form': user_form, 'counselor_form': counselor_form})

    else:
       message = 'You must be logged in to view this!'
       messages.error(request, message)
       return redirect(reverse('Home:login'))


class CounselorChangePasswordView(SuccessMessageMixin, PasswordChangeView):
   template_name = 'changecounselorpassword.html'
   success_url = reverse_lazy('CounselorProfile:counselorprofile')   #URL to redirect to after the password is successfully changed
   success_message = "Password successfully changed."   #displayed after the password is successfully changed

   def form_valid(self, form):   #called when the password change form is valid
        response = super().form_valid(form)
        return response  