from django.urls import path
from . import views

app_name = "StudentProfile"

urlpatterns = [
    path('profile/', views.ProfileView, name="studentprofile"),
    path('editprofile/', views.EditProfileView, name="studentedit"),
    path('changepassword/', views.StudentChangePasswordView.as_view(), name='studentchangepassword'),
]

 