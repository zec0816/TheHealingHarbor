from django.shortcuts import redirect, render
from .models import Diary
from django.contrib.auth.decorators import login_required
from Home.decorators import student_required

# Create your views here.

@student_required
def diary(request):
    diary=Diary.objects.all() 
    return render(request,'studentdiary.html',{'diary':diary})

@student_required
def diaryadd(request):
    return render(request,'studentadddiary.html')

@student_required
def diaryaddrec(request): 
    if request.method == 'POST':
      v=request.POST['title']
      w=request.POST['diary']
      x=request.user.student
      diary=Diary(student=x,title=v,diary=w)
      diary.save()
      return redirect('StudentDiary:diary')

@student_required 
def diarydelete(request,id):
    diary=Diary.objects.get(id=id)
    diary.delete()
    return redirect('StudentDiary:diary')

@student_required 
def diaryupdate(request,id):
    diary=Diary.objects.get(id=id)
    return render(request,'studentupdatediary.html',{'diary':diary})

@student_required 
def diaryuprec(request,id):       
    v=request.POST['title']
    w=request.POST['diary']
    diary=Diary.objects.get(id=id)
    diary.title=v
    diary.diary=w
    diary.save()
    return redirect('StudentDiary:diary')