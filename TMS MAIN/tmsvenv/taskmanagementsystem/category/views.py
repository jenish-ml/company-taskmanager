from django.shortcuts import render,redirect
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def add_category(request):
    form=CategoryForm(request.POST)
    if(request.method=='POST'):
        if form.is_valid():
            form.save()
        return redirect('/view_category')
    else:
        form=CategoryForm()
        return render(request,'add_category.html',{'form':form})
    
@login_required(login_url='/login')
def view_category(request):
    a=Category.objects.all()
    search = request.GET.get('search','')
    if search:
        a = a.filter(Q(categories__icontains=search))
        print(a)
    return render(request,'view_category.html',{'a':a})

@login_required(login_url='/login')
def edit_category(request,id):
    data = Category.objects.get(id=id)
    print(data)
    form = CategoryForm(request.POST,instance=data)
    if form.is_valid():
        data.save()
        form.save()
        return redirect('/view_category')
    else:
        form = CategoryForm(instance=data)
        return render(request,'add_category.html',{'form':form})
    
@login_required(login_url='/login')
def delete_category(request,id):
    a=Category.objects.get(id=id)
    a.delete()
    return redirect('/view_category')