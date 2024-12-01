from django.shortcuts import redirect, render
from .models import Info
from django.contrib.auth.decorators import login_required
from Home.decorators import counselor_required

# Create your views here.

@counselor_required
def info(request):

    """Displays information posted by the logged in counselor."""

    info=Info.objects.all() 
    return render(request,'counselorinfosection.html',{'info':info})

@counselor_required
def infoadd(request):
    return render(request,'counseloraddinfo.html')

@counselor_required
def infoaddrec(request): #add info
    if request.method == 'POST':
      v=request.POST['title']
      w=request.POST['info']
      x=request.user.counselor
      info=Info(counselor=x,title=v,info=w)
      info.save()
      return redirect('infosection:info')

@counselor_required #delete info
def infodelete(request,id):
    info=Info.objects.get(id=id)
    info.delete()
    return redirect('infosection:info')

@counselor_required #get the id of the info to update
def infoupdate(request,id):
    info=Info.objects.get(id=id)
    return render(request,'counselorupdateinfo.html',{'info':info})

@counselor_required #update info
def infouprec(request,id):       
    v=request.POST['title']
    w=request.POST['info']
    info=Info.objects.get(id=id)
    info.title=v
    info.info=w
    info.save()
    return redirect('infosection:info')