from django.shortcuts import render,redirect
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def designation(request):
    form = DesignationForm(request.POST)
    if(request.method=='POST'):
        if form.is_valid():
            form.save()
        return redirect('/view_role')
    else:
        form = DesignationForm()
        return render(request,'add_role.html',{'form':form})
    
@login_required(login_url='/login')
def designation_view(request):
    a = Role.objects.all()
    search = request.GET.get('search','')
    if search:
        a = a.filter(Q(role__icontains=search))
        print(a)
    return render(request,'view_role.html',{'a':a})

@login_required(login_url='/login')       
def designation_edit(request,id):
    data = Role.objects.get(id=id)
    form = DesignationForm(request.POST,instance=data)
    if form.is_valid():
        data.save()
        form.save()
        return redirect('/view_role')
    else:
        form = DesignationForm(instance=data)
        return render(request,'add_role.html',{'form':form})

@login_required(login_url='/login') 
def designation_delete(request,id):
    a = Role.objects.get(id=id)
    a.delete()
    return redirect('/view_role')