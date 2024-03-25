from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from Files.models import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# function of add message
def statusadd(request, id):
    task = Task.objects.get(id=id)
    project = Projects.objects.get(task=task)
    if request.method == 'POST':
        form = StatusAddForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save(commit=False)
            status.task = task
            status.project = project
            status.userid = Register.objects.get(id=request.user.id)
            status.save()
            files = request.FILES.getlist('file')
            if files:
                for file in files:
                    upload_file = UploadFile(file=file)
                    upload_file.save()
                    status.file.add(upload_file)
            TaskHistory.objects.create(
                message = 1,
                project = project,
                modified_by = request.user,
                modified_at = timezone.now(), 
                task = task
            )
            return redirect(reverse('view_task', args=[task.id]))
    else:
        form = StatusAddForm()
    return render(request, 'add_status.html', {'form': form})

# def statusview(request):
#     search = request.GET.get('search', '')
#     filter = request.GET.get('filter', '')
#     a = Status.objects.all()
#     if search:
#         a = a.filter(Q(current_status__icontains=search) | Q(message__icontains=search) | Q(task__title__icontains = search) | Q(project__title__icontains=search))
#     if filter:
#         a = a.filter(current_status=filter)
#     return render(request, 'view_status.html', {'a': a, 'search': search})

# message edit
def statusedit(request, id):
    status = Status.objects.get(id=id)
    task = status.task
    related_files = status.file.all()
    if request.method == 'POST':
        form = StatusEditForm(request.POST, request.FILES, instance=status)
        if form.is_valid():
            updated_status = form.save(commit=False)
            updated_status.save()
            files = request.FILES.getlist('file')
            if files:
                for file in files:
                    updated_status.file.create(file=file)
            files_to_remove = request.POST.getlist('remove_files')
            for file_id in files_to_remove:
                file_to_remove = UploadFile.objects.get(id=file_id)
                file_to_remove.file.delete()
                file_to_remove.delete()
            return redirect(reverse('view_task', args=[task.id]))
    else:
        form = StatusEditForm(instance=status)
    return render(request, 'edit_status.html', {'form': form, 'status': status, 'related_files': related_files})


def statusdelete(request,id):
    a = Status.objects.get(id=id)
    task = a.task
    a.delete()
    return redirect(reverse('view_task', args=[task.id]))

# @login_required(login_url='/login')
# def statusesadd(request,id):
#     task = Task.objects.get(id=id)
#     project = Projects.objects.get(task=task)
#     if request.method == 'POST':
#         form = StatusesAddForm(request.POST,request.FILES,instance=task)
#         if form.is_valid():
#             task.statuses = form.cleaned_data['statuses']
#             task.messages = form.cleaned_data['messages']
#             task.save()
#         project_id = task.project.id
#         url = reverse('view_task_statuses', args=[project_id])
#         return redirect(url)
#     else:
#         form = StatusesAddForm(instance=task)
#     return render(request,'add_status.html',{'form':form})
    
# @login_required(login_url='/login')
# def statusesview(request):
#     search = request.GET.get('search', '')
#     filter = request.GET.get('filter', '')
#     a = Task.objects.all()
#     b = request.user.id
#     c = Task.objects.filter(staff=b)
#     if search:
#         a = a.filter(Q(statuses__icontains=search) | Q(messages__icontains=search) | Q(title__icontains = search) | Q(project__title__icontains=search))
#     if filter:
#         a = a.filter(statuses=filter)
#     return render(request, 'view_statuses.html', {'a': a,'c':c, 'search': search})

def taskstatusview(request,id):
    a = Projects.objects.get(id=id)
    b = Task.objects.filter(project=a)
    c = request.user.id
    d = Task.objects.filter(project=a,staff=c)
    search = request.GET.get('search', '')
    filter = request.GET.get('filter', '')
    if search:
        b = b.filter(Q(statuses__icontains=search) | Q(messages__icontains=search) | Q(title__icontains = search) | Q(project__title__icontains=search))
        d = d.filter(Q(statuses__icontains=search) | Q(messages__icontains=search) | Q(title__icontains = search) | Q(project__title__icontains=search))
    if filter:
        b = b.filter(statuses=filter)
        d = d.filter(statuses=filter)
    return render(request,'view_task_statuses.html',{'b':b,'a':a,'d':d,'search': search,'filter': filter})

# @login_required(login_url='/login')
# def statusadd(request,id):
#     task = Task.objects.get(id=id)
#     project = Projects.objects.get(task=task)
#     if request.method == 'POST':
#         form = StatusAddForm(request.POST,request.FILES,instance=task)
#         if form.is_valid():
#             task.statuses = form.cleaned_data['statuses']
#             task.messages = form.cleaned_data['messages']
#             task.save()
#         return redirect('/view_project')
#     else:
#         form = StatusAddForm(instance=task)
#     return render(request,'add_status.html',{'form':form})

