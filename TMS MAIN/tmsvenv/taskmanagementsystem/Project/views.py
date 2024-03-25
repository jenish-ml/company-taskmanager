from django.shortcuts import render, redirect
from .forms import *
from .models import Projects
from django.db.models import Q,Count
from datetime import datetime
from Status.models import *
from django.core.mail import send_mail
from django.conf import settings
from Tasks.forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


@login_required(login_url='/login')
def projectadd(request):
    if request.method == 'POST':
        form = ProjectAddForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.current_date = datetime.now()
            project.created_by = request.user
            project.save()

            team_members = project.team.team_members.all()
            files = request.FILES.getlist('file_field')  # Use 'file_field' instead of 'file'

            if files:
                for file in files:
                    upload_file = UploadFile(file=file)
                    upload_file.save()
                    project.file.add(upload_file)

            send_mail(
                subject="Assigned Project",
                message=f"Admin Assigned a project: {project.title} And Your Due Date is: {project.due_date}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[i.email for i in team_members]
            )
            return redirect('/view_project', project.id)
    else:
        form = ProjectAddForm()

    return render(request, 'add_project.html', {'form': form})
    
def projectview(request):
    all_projects = Projects.objects.all()
    search = request.GET.get('search', '')
    selected_project_title = request.GET.get('filter', '') 
    selected_staff_member_name = request.GET.get('staff_filter', '')
    if search:
        all_projects = all_projects.filter(Q(title__icontains=search) | Q(team__team_members__name__icontains=search))
    if selected_project_title:
        all_projects = all_projects.filter(title=selected_project_title)
    staff_members = Register.objects.exclude(usertype=1)
    distinct_project_titles = Projects.objects.values_list('title', flat=True).distinct()
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
    context = {
        'all_projects': all_projects,
        'selected_project_title': selected_project_title,
        'distinct_project_titles': distinct_project_titles,
        'staff_member': staff_members,
        'distinct_staff_member': distinct_staff_member,
        'selected_staff_member': selected_staff_member_name,
    }
    return render(request, 'view_project.html', context)



@login_required(login_url='/login')
def projectedit(request, id):
    project = Projects.objects.get(id=id)
    related_files = project.file.all()

    if request.method == 'POST':
        form = ProjectEditForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            updated_project = form.save(commit=False)
            updated_project.current_date = timezone.now()
            updated_project.updated_by = request.user
            updated_project.save()
            team_members = project.team.team_members.all()

            files = request.FILES.getlist('file_field') 
            for file in files:
                upload_file = UploadFile(file=file)
                upload_file.save()
                updated_project.file.add(upload_file)

            files_to_remove = request.POST.getlist('remove_files')
            for file_id in files_to_remove:
                file_to_remove = UploadFile.objects.get(id=file_id)
                file_to_remove.file.delete()
                updated_project.file.remove(file_to_remove)

            send_mail(
                subject="Updated Project",
                message=f"Admin Updated a project: {project.title} And Your Due Date is: {project.due_date}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[i.email for i in team_members]
            )
            return redirect(reverse('view_project_index', args=[project.id]))
    else:
        form = ProjectEditForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project, 'related_files': related_files})

@login_required(login_url='/login')    
def projectdelete(request,id):
    a = Projects.objects.get(id=id)
    a.delete()
    return redirect('/view_project')

def projectviewindex(request, id):
    c = Projects.objects.get(id=id)
    a = Projects.objects.filter(id=id)
    b = Task.objects.filter(project=id)
    d = Team.objects.filter(projects=id)
    e = request.user.id
    usertype = request.session.get('ut', 0)
    f = Task.objects.filter(staff=e, project=id)
    if usertype == 3:
        task_counts = f.values('status').annotate(count=Count('id'))
    else:
        task_counts = b.values('status').annotate(count=Count('id'))
    New_count = 0
    In_Progress_count = 0
    Completed_count = 0
    Resolved_count = 0
    Reopen_count = 0
    for task_count in task_counts:
        status = task_count.get('status')
        count = task_count.get('count')
        if status == 'New':
            New_count = count
        elif status == 'In Progress':
            In_Progress_count = count
        elif status == 'Completed':
            Completed_count = count
        elif status == 'Resolved':
            Resolved_count = count
        elif status == 'Reopen':
            Reopen_count = count
    priority_filter = request.GET.get('priority-filter','')
    category_filter = request.GET.get('category-filter','')
    status_filter = request.GET.get('status-filter','')
    staff_filter = request.GET.get('staff-filter','')
    if priority_filter:
        b = b.filter(priority=priority_filter)
    if category_filter:
        b = b.filter(category=category_filter)
    if status_filter:
        b = b.filter(status=status_filter)
    if staff_filter:
        b = b.filter(staff__name=staff_filter)
    staff_members = Register.objects.exclude(usertype=1)
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    
    return render(request, 'view_project_index.html', {'priority_filter':priority_filter,'staff_filter':staff_filter,'category_filter':category_filter,'status_filter':status_filter,'staff_member': staff_members,'distinct_staff_member':distinct_staff_member,'a': a, 'b': b, 'c': c, 'd': d, 'f': f,'New_count':New_count,'In_Progress_count':In_Progress_count,'Completed_count':Completed_count,'Resolved_count':Resolved_count,'Reopen_count':Reopen_count})


def view_staff_project_index(request):
    a = request.user.id
    all_projects = Projects.objects.filter(team__team_members=a)
    c = Task.objects.filter(staff=a)
    print(c)
    selected_project_title = request.GET.get('filter', '')
    selected_staff_member_name = request.GET.get('staff_filter', '')
    search = request.GET.get('search', '')
    if search:
        all_projects = all_projects.filter(Q(title__icontains=search))
    if selected_project_title:
        all_projects = all_projects.filter(title=selected_project_title)
        c = c.filter(project__title=selected_project_title)
    staff_members = Register.objects.exclude(usertype=1)
    distinct_project_titles = Projects.objects.values_list('title', flat=True).distinct()
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
        c = c.filter(Q(team__team_members__name=selected_staff_member_name))

    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
    context = {
        'c':c,
        'all_projects': all_projects,
        'selected_project_title': selected_project_title,
        'distinct_project_titles': distinct_project_titles,
        'staff_member': staff_members,
        'distinct_staff_member': distinct_staff_member,
        'selected_staff_member': selected_staff_member_name,
    }
    return render(request, 'view_staff_project_index.html',context)
    
def projectview(request):
    all_projects = Projects.objects.all()
    search = request.GET.get('search', '')
    selected_project_title = request.GET.get('filter', '') 
    selected_staff_member_name = request.GET.get('staff_filter', '')
    if search:
        all_projects = all_projects.filter(Q(title__icontains=search) | Q(team__team_members__name__icontains=search))
    if selected_project_title:
        all_projects = all_projects.filter(title=selected_project_title)
    staff_members = Register.objects.exclude(usertype=1)
    distinct_project_titles = Projects.objects.values_list('title', flat=True).distinct()
    distinct_staff_member = Register.objects.exclude(usertype=1).values_list('name', flat=True).distinct()
    if selected_staff_member_name:
        all_projects = all_projects.filter(Q(team__team_members__name__icontains=selected_staff_member_name))
    context = {
        'all_projects': all_projects,
        'selected_project_title': selected_project_title,
        'distinct_project_titles': distinct_project_titles,
        'staff_member': staff_members,
        'distinct_staff_member': distinct_staff_member,
        'selected_staff_member': selected_staff_member_name,
    }
    return render(request, 'view_project.html', context)
