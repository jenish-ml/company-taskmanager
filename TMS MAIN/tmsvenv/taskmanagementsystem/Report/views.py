from django.shortcuts import render,redirect
from Tasks.models import Task
from Project.models import Projects
from .forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def viewreport(request):
    a = []
    if request.method=='POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            a = Task.objects.filter(start_date__gte=start_date, due_date__lte=end_date)
            print(a)
            return render(request,'view_report.html', {'a':a})
    else:
        form = ReportForm()
    return render(request,'view_report.html', {'form': form,'a':a})

@login_required(login_url='/login')
def viewreport(request,id):
    project = Projects.objects.get(id=id)
    a = []
    if request.method=='POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            a = Task.objects.filter(start_date__gte=start_date, due_date__lte=end_date,project=project)
            print(a)
            return render(request,'view_report.html', {'a':a,'project':project})
    else:
        form = ReportForm()
    return render(request,'view_report.html', {'form': form,'a':a,'project':project})

