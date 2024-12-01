from django.urls import path
from . import views

app_name = "StudentHomePage"

urlpatterns = [
    path('', views.IndexView, name="index"),
]