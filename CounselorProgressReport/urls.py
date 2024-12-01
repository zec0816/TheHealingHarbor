from django.urls import path
from .views import display_scores

app_name = "CounselorProgressReport"

urlpatterns = [
    path('progress/', display_scores, name="progress"),
    #path('progress/', chart_view, name="progress"),
]
