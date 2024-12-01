from django.shortcuts import render

# Create your views here.
def TestimonialView(request):
    return render(request, 'testimonial.html')
