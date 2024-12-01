from django.urls import path
from . import views

app_name = "Home"

urlpatterns = [
    path('', views.HomeView, name='home'),
    path("signup/", views.RegistrationView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView, name='logout'),
]