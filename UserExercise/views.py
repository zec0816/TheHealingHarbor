from django.shortcuts import render

# Create your views here.

def exercises_page(request):
    return render(request, 'exercise.html')
