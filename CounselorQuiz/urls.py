from django.urls import path
from . import views

app_name = "CounselorQuiz"

urlpatterns = [
    path('questions/', views.quiz_question_list, name='quiz_question_list'),
    path('questions/create/', views.quiz_question_create, name='quiz_question_create'),
    path('questions/update/<int:question_id>/', views.quiz_question_update, name='quiz_question_update'),
    path('questions/delete/<int:question_id>/', views.quiz_question_delete, name='quiz_question_delete'),
]