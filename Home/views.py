from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import RegistrationForm, LoginForm
from .models import Student, Counselor, User
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from django.utils import timezone


# Create your views here.
def HomeView(request):
    return render(request, 'homepage.html')

class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'signup.html'   #redirect to this template if registrationview is accessed

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):   #submitted
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']        #get data from form
            role = form.cleaned_data['role']
            if role == 'counselor':
                user.is_counselor = True            #If counselor, set the is_counselor flag and create a Counselor instance
                counselor = Counselor.objects.create(user=user, full_name=full_name, phone_number=phone_number, created_at=timezone.now())
                counselor.save()
            elif role == 'student':
                user.is_student = True             #If student, set the is_student flag and create a Student instance
                student = Student.objects.create(user=user, full_name=full_name, phone_number=phone_number, created_at=timezone.now())
                student.save()

            message = f"Account created successfully for {full_name}"
            messages.success(request, message)
            return redirect(reverse('Home:login'))

        return render(request, self.template_name, {'form': form})
    
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_student:                             #different pages for student and counselor (and superuser)
                return reverse('StudentHomePage:index')
            elif user.is_counselor:
                return reverse('infosection:info')
            else:
                return reverse('admin:index')
        else:
            return reverse('Home:login')

@never_cache
def LogoutView(request):         #logout
    logout(request)
    return redirect(reverse('Home:home'))