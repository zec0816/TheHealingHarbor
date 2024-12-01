from django.urls import path
from . import views

app_name = "UserTestimonial"

urlpatterns = [
    path('testimonial/',views.TestimonialView, name="testimonial"),
]
