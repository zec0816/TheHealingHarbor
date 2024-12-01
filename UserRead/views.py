from django.shortcuts import render

# Create your views here.
def ReadView(request):
    return render(request, 'read.html')

def Book1View(request):
    return render(request, 'book1.html')

def Book2View(request):
    return render(request, 'book2.html')

def Book3View(request):
    return render(request, 'book3.html')

def Book4View(request):
    return render(request, 'book4.html')

def Book5View(request):
    return render(request, 'book5.html')