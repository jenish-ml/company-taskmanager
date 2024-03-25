from django.shortcuts import render,redirect
from datetime import datetime,timedelta
from .models import *
from .forms import *
from django.db.models import Q
from Status.models import Status
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Team.models import *
from Status.forms import *
# Create your views here.

# @login_required(login_url='/login')
# def taskadd(request,id):
#     project = Projects.objects.get(id=id)
#     team_members = project.team.team_members.all()
#     form = TaskAddForm(request.POST,request.FILES)
#     if request.method == 'POST':
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.current_date = datetime.now()
#             task.project=project
#             task.save()
#             files = request.FILES.getlist('file')
#             if files:
#                 for file in files:
#                     task.file.create(file=file)
#             send_mail(
#                 subject="Assigned Project",
#                 message=f"Admin Assigned a task: {task.title} "f" And Your Due Date is: {task.due_date}"f"And your task priority is {task.priority}",
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[task.staff.email]
#             )
#             return redirect('/view_project')
#     else:
#         form = TaskAddForm()
#     return render(request,'add_task.html',{'form':form,'project':project,'team_members':team_members})

@login_required(login_url='/login')
def taskadd(request, id):
    project = Projects.objects.get(id=id)
    print(project)
    team_members = project.team.team_members.all()
    members = [member.name for member in team_members]
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')
        due_date_datetime = datetime.strptime(due_date, '%Y-%m-%d')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        staff = request.POST.get('staff')
        status = "New"
        staff_member = Register.objects.get(name=staff)
        assigned_by = request.user.id
        assigned_staff=Register.objects.get(id=assigned_by)
        task = Task.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            due_date=due_date,
            priority=priority,
            category=category,
            project=project,
            staff=staff_member,
            assigned_staff=assigned_staff,
            status=status,
            created_by=request.user
        )
        # ProjectHistory.objects.create(
        #     project = project,
        #     modified_by = request.user,
        #     modified_date = timezone.now(), 
        #     task_add = 1,
        #     task = title
        # )
        files = request.FILES.getlist('file')
        for uploaded_file in files:
            upload_file = UploadFile.objects.create(file=uploaded_file)
            task.file.add(upload_file)
        send_mail(
                subject="Assigned Project",
                message=f"{assigned_staff.name} Assigned a task: {task.title} "f" And Your Due Date is: {task.due_date}"f"And your task priority is {task.priority}" " for more details check the website",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [task.staff.email]
            )
        yesterday = timezone.now() - timedelta(days=1)
        if due_date_datetime.date() == yesterday.date():
            send_mail(
                subject="Task Reminder",
                message=f"Reminder: Your task '{task.title}' was due yesterday. Please complete it as soon as possible.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[task.staff.email]
            )
        return redirect(reverse('view_project_index', args=[project.id]))
    return render(request, 'add_task.html', {'project': project, 'members': members, 'team_members': team_members})

@login_required(login_url='/login')
def taskview(request):
    a = Task.objects.all()
    b = request.user.id
    c = Task.objects.filter(staff=b)
    # d = Task.objects.filter(team__team_members=b)
    search = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')
    status_filter = request.GET.get('filter', '')
    if search:
        a = a.filter(Q(project__title__icontains=search) | Q(title__icontains=search) | Q(category__categories__icontains=search))  
        c = c.filter(Q(project__title__icontains=search) | Q(title__icontains=search) | Q(category__categories__icontains=search))  
    if priority_filter:
        a = a.filter(priority=priority_filter)
        c = c.filter(priority=priority_filter)
    if status_filter:
        a = a.filter(statuses=status_filter)
        c = c.filter(statuses=status_filter)
    return render(request, 'view_task.html', {'a': a, 'c': c, })

@login_required(login_url='/login')
def taskdelete(request,id):
    a = Task.objects.get(id=id)
    task = a.title
    project = a.project
    a.delete()
    # ProjectHistory.objects.create(
    #     project = project,
    #     modified_by = request.user,
    #     modified_date = timezone.now(), 
    #     task_delete = 1,
    #     task = task
    # )
    return redirect(reverse('view_project_index', args=[project.id]))

# @login_required(login_url='/login')
# def taskedit(request, id):
#     task = Task.objects.get(id=id)
#     related_files = task.file.all()
#     if request.method == 'POST':
#         form = TaskEditForm(request.POST, request.FILES, instance=task)
#         if form.is_valid():
#             updated_task = form.save(commit=False)
#             updated_task.save()
#             files = request.FILES.getlist('file')
#             if files:
#                 for file in files:
#                     task.file.create(file=file)
#             files_to_remove = request.POST.getlist('remove_files')
#             for file_id in files_to_remove:
#                 file_to_remove = UploadFile.objects.get(id=file_id)
#                 file_to_remove.file.delete()
#                 task.file.remove(file_to_remove) 
#             project_id = task.project.id
#             url = reverse('view_project_task', args=[project_id])
#             return redirect(url)
#     else:
#         form = TaskEditForm(instance=task)
#     return render(request, 'edit_task.html', {'task': task, 'form': form, 'related_files': related_files})

@login_required(login_url='/login')
def taskedit(request, id):
    task = Task.objects.get(id=id)
    a = task.project.id
    project = Projects.objects.get(id=a)
    team_members = project.team.team_members.all()
    members = [member.name for member in team_members]
    related_files = task.file.all()
    current_staff = task.staff.name if task.staff else None
    assigned_by = request.user.id
    assigned_staff=Register.objects.get(id=assigned_by)
    old_title = task.title
    old_description = task.description
    old_start_date = task.start_date
    old_due_date = task.due_date
    old_priority = task.priority
    old_category = task.category
    old_status = task.status
    old_staff = task.staff
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save(commit=False)
            staff_name = request.POST.get('staff')
            if staff_name:
                staff = Register.objects.get(name=staff_name)
                updated_task.staff = staff
            updated_task.assigned_staff = assigned_staff
            updated_task.save()
            TaskHistory.objects.create(
                task=task,
                project=project,
                modified_by = request.user,
                modified_at = timezone.now(),
                old_title = old_title,
                new_title = updated_task.title,
                old_description = old_description,
                new_description = updated_task.description,
                old_start_date = old_start_date,
                new_start_date = updated_task.start_date,
                old_due_date = old_due_date,
                new_due_date = updated_task.due_date,
                old_priority = old_priority,
                new_priority = updated_task.priority,
                old_category = old_category,
                new_category = updated_task.category,
                old_status = old_status,
                new_status = updated_task.status,
                old_staff = old_staff,
                new_staff = updated_task.staff
            )
            files = request.FILES.getlist('file')
            if files:
                for file in files:
                    task.file.create(file=file)
                    TaskHistory.objects.create(
                        task=task,
                        project=project,
                        modified_by = request.user,
                        modified_at = timezone.now(),
                        file_status = "1"
                    )
            files_to_remove = request.POST.getlist('remove_files')
            for file_id in files_to_remove:
                file_to_remove = UploadFile.objects.get(id=file_id)
                file_to_remove.file.delete()
                task.file.remove(file_to_remove)
                TaskHistory.objects.create(
                        task=task,
                        project=project,
                        modified_by = request.user,
                        modified_at = timezone.now(),
                        file_remove_status = "1"
                    )
            send_mail(
            subject="Assigned Task",
            message=f"{assigned_staff.name} Assigned a task: {task.title} "f" And Your Due Date is: {task.due_date}"f"And your task priority is {task.priority}" " for more details check the website",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list = [task.staff.email]
            )
            return redirect(reverse('view_task', args=[task.id]))
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'edit_tasks.html', {'form': form, 'members': members, 'related_files': related_files, 'current_staff': current_staff})


@login_required(login_url='/login')
def view_project_details(request,id):
    b = Task.objects.get(id=id)
    c = b.project.id
    d = Projects.objects.filter(id=c)
    return render(request,'view_assigned_project.html',{'d':d})

# @login_required(login_url='/login')
# def task_performance_analysises(request):
#     task_counts = Task.objects.values('statuses').annotate(count=Count('id'))
#     to_do_count = 0
#     in_progress_count = 0
#     completed_count = 0
#     for task_count in task_counts:
#         status = task_count.get('statuses')
#         count = task_count.get('count')
#         if status == 'to-do':
#             to_do_count = count
#         elif status == 'in progress':
#             in_progress_count = count
#         elif status == 'completed':
#             completed_count = count
#     context = {
#         'to_do_count': to_do_count,
#         'in_progress_count': in_progress_count,
#         'completed_count': completed_count,
#     }
#     return render(request, 'view_tasks.html', context)

@login_required(login_url='/login')
def taskprojectview(request, id):
    b = Projects.objects.get(id=id)
    a = Task.objects.filter(project=id)
    c = request.user.id
    d = Task.objects.filter(staff=c)
    e = Status.objects.filter(userid=c)
    print(e)
    search = request.GET.get('search', '')
    priority_filter = request.GET.get('priority', '')
    status_filter = request.GET.get('filter', '')
    if search:
        a = a.filter(Q(project__title__icontains=search) | Q(title__icontains=search) | Q(category__categories__icontains=search))
        d = d.filter(Q(project__title__icontains=search) |Q(title__icontains=search) | Q(category__categories__icontains=search))
    if priority_filter:
        a = a.filter(priority=priority_filter)
        d = d.filter(priority=priority_filter)
    if status_filter:
        a = a.filter(statuses=status_filter)
        d = d.filter(statuses=status_filter)
    return render(request, 'view_project_task.html', {'a': a, 'b': b, 'd': d, 'e':e})

# def task_performance_analysis(request, project_id):
#     a=Projects.objects.get(id=project_id)
#     task_counts = Task.objects.filter(project_id=project_id).values('statuses').annotate(count=Count('id'))
#     to_do_count = 0
#     in_progress_count = 0
#     completed_count = 0
#     for task_count in task_counts:
#         status = task_count.get('statuses')
#         count = task_count.get('count')
#         if status == 'to-do':
#             to_do_count = count
#         elif status == 'in progress':
#             in_progress_count = count
#         elif status == 'completed':
#             completed_count = count
#     context = {
#         'to_do_count': to_do_count,
#         'in_progress_count': in_progress_count,
#         'completed_count': completed_count,
#         'a': a,
#     }
#     return render(request, 'project_task_performance.html', context)

@login_required(login_url='/login')
def view_main_task(request,id):
    a = Task.objects.get(id=id)
    b = Task.objects.filter(id=id)
    c = request.user.id
    g = Register.objects.get(id=c)
    d = Status.objects.filter(task=a).order_by('current_date')
    e = Status.objects.filter(userid=c,task=a)
    f = Task.objects.filter(parent_task=a).all()
    # h = SubTask.objects.filter(task=a,staff=g)
    task_history = TaskHistory.objects.filter(task = a).order_by('modified_at')
    return render(request,'view_main_task.html',{'a':a,'b':b, 'd':d, 'e':e, 'f':f,'task_history':task_history})

@login_required(login_url='/login')
def subtaskadd(request, id):
    task = Task.objects.get(id=id)
    print(task)
    t = task.id
    project_id = task.project_id
    project = Projects.objects.get(id=project_id)
    team_members = project.team.team_members.all()
    members = [member.name for member in team_members]
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        staff = request.POST.get('staff')
        status = "New"
        staff_member = Register.objects.get(name=staff)
        assigned_by = request.user.id
        assigned_staff=Register.objects.get(id=assigned_by)
        Task.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            due_date=due_date,
            priority=priority,
            category=category,
            project=project,
            staff=staff_member,
            assigned_staff=assigned_staff,
            status=status,
            parent_task=task
        )
        TaskHistory.objects.create(
            task=task,
            project=project,
            modified_by = request.user,
            modified_at = timezone.now(),
            subtask_add = 1,
            subtask = title
        )
        files = request.FILES.getlist('file')
        for uploaded_file in files:
            upload_file = UploadFile.objects.create(file=uploaded_file)
            task.file.add(upload_file)
        send_mail(
                subject="Assigned Project",
                message=f"{assigned_staff.name} Assigned a task: {task.title} "f" And Your Due Date is: {task.due_date}"f"And your task priority is {task.priority}" " for more details check the website",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [task.staff.email]
            )
        return redirect(reverse('view_task', args=[t]))
    return render(request, 'add_subtask.html', {'project': project,'task':task, 'members': members, 'team_members': team_members})

@login_required(login_url='/login')
def subtaskview(request,id):
    subtask = Task.objects.get(id=id)
    a = subtask.id
    print(a)
    c = Task.objects.get(id=a)
    e = request.user.id
    b = Task.objects.filter(id=id)
    print(b)
    d = Subtaskmessage.objects.filter(task=a)
    return render(request,'view_subtask.html',{'b':b,'d':d})

@login_required(login_url='/login')
def subtaskedit(request, id):
    subtask = Task.objects.get(id=id)
    a = subtask.id
    task = Task.objects.get(id=a)
    project = task.project
    team_members = project.team.team_members.all()
    members = [member.name for member in team_members]
    related_files = subtask.file.all()
    current_staff = subtask.staff.name if subtask.staff else None
    assigned_by = request.user.id
    assigned_staff = Register.objects.get(id=assigned_by)
    if request.method == 'POST':
        form = SubTaskEditForm(request.POST, instance=subtask)
        if form.is_valid():
            updated_subtask = form.save(commit=False)
            staff_name = request.POST.get('staff')
            if staff_name:
                staff = Register.objects.get(name=staff_name)
                updated_subtask.staff = staff
            updated_subtask.assigned_staff = assigned_staff
            updated_subtask.save()
            files = request.FILES.getlist('file')
            for uploaded_file in files:
                subtask.file.create(file=uploaded_file)
            files_to_remove = request.POST.getlist('remove_files')
            for file_id in files_to_remove:
                file_to_remove = UploadFile.objects.get(id=file_id)
                file_to_remove.file.delete()
                subtask.file.remove(file_to_remove)
            send_mail(
                subject="Updated Subtask",
                message=f"{assigned_staff.name} updated the subtask: {subtask.title} "f" with a due date of {subtask.due_date}"f"and priority {subtask.priority}. Check the website for more details.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subtask.staff.email]
            )
            return redirect(reverse('view_subtask', args=[subtask.id]))
    else:
        form = SubTaskEditForm(instance=subtask)
    return render(request, 'edit_subtask.html', {
        'form': form,
        'members': members,
        'related_files': related_files,
        'current_staff': current_staff
    })
    
@login_required(login_url='/login')
def subtaskdelete(request,id):
    a = Task.objects.get(id=id)
    task = a.task
    title = a.title
    print(task)
    project = a.task.project
    print(project)
    a.delete()
    TaskHistory.objects.create(
        task=task,
        project=project,
        modified_by = request.user,
        modified_at = timezone.now(),
        subtask_delete = 1,
        subtask = title
    )
    return redirect(reverse('view_task', args=[task.id]))

@login_required(login_url='/login')
def statusupdate(request, id):
    task = Task.objects.get(id=id)
    status = task.status
    project = task.project
    assigned_by = request.user.id
    assigned_staff = Register.objects.get(id=assigned_by)
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            TaskHistory.objects.create(
                task=task,
                project=project,
                modified_by = request.user,
                modified_at = timezone.now(),
                old_status = status,
                new_status = task.status
            )
            if request.user.usertype in [1, 2]:
                send_mail(
                    subject="Updated Subtask",
                    message=f"{assigned_staff.name} updated the task: {task.title} "
                            f"status into {task.status}. "
                            f"Check the website for more details.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[task.staff.email]
                )
            return redirect('view_task', id=task.id)
    else:
        form = TaskStatusForm(instance=task)
    return render(request, 'apply_status.html', {'form': form})

@login_required(login_url='/login')
def subtaskmessage(request, id):
    subtask = Task.objects.get(id=id)
    task = subtask.task
    project = task.project
    if request.method == 'POST':
        form = MessageAddForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save(commit=False)
            status.task = task 
            status.project = project
            status.userid = Register.objects.get(id=request.user.id)
            status.save()
            files = request.FILES.getlist('file')
            if files:
                for file in files:
                    status.file.create(file=file)
            return redirect(reverse('view_subtask', args=[subtask.id]))
    else:
        form = MessageAddForm()
    return render(request, 'add_subtask_message.html', {'form': form})
