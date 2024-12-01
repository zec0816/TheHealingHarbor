from django.urls import path
from . import views

app_name = "CounselorProfile"

urlpatterns = [
    path('profile/', views.ProfileView, name="counselorprofile"),
    path('editprofile/', views.EditProfileView, name="counseloredit"),
    path('changepassword/', views.CounselorChangePasswordView.as_view(), name='counselorchangepassword'),
]

 