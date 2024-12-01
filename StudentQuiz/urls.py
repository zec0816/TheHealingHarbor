from django.urls import path
from . import views

app_name = "StudentQuiz"

urlpatterns = [
    path('quiz/',views.QuestionView,name="quiz"),
    path('quiz/result/', views.ScoreView,name="result"),
]
