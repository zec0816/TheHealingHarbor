from django.urls import path
from . import views

app_name = "UserExercise"

urlpatterns = [
    path('exercise/',views.exercises_page,name="exercise"),
]
