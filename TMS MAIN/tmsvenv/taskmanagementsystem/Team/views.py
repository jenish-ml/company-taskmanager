from django.shortcuts import render,redirect
from .forms import *
from django.db.models import Q
from Project.models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from Tasks.models import *

# Create your views here.
# def teamadd(request):
#     form = TeamAddForm(request.POST)
#     if request.method=='POST':
#         if form.is_valid():
#             form.save()
#         return redirect('/view_team')
#     else:
#         form = TeamAddForm()
#         return render(request,'add_team.html',{'form':form})
    
# def teamview(request):
#     a = Teams.objects.all()
#     search = request.GET.get('search','')
#     if search:
#         a = a.filter(Q(team_name__icontains=search))
#         print(a)
#     return render(request,'view_team.html',{'a':a})

# def teamedit(request,id):
#     data = Teams.objects.get(id=id)
#     if request.method == 'POST':
#         form = TeamAddForm(request.POST,instance=data)
#         if form.is_valid():
#             data.save()
#         return redirect("/view_team")
#     else:
#         form = TeamAddForm(instance=data)
#         return render(request,'add_team.html',{'form':form})

# def teamdelete(request,id):
#     a = Teams.objects.get(id=id)
#     a.delete()
#     return redirect('/view_team')
        
# def teammembersadd(request, id):
#     team = Teams.objects.get(id=id)
#     if request.method == "POST":
#         form = TeamMembersAddForm(request.POST)
#         if form.is_valid():
#             team_members = form.cleaned_data['team_members']
#             team_member_instance = Team_members.objects.create(team=team)
#             team_member_instance.team_members.add(*team_members)
#             return redirect('/view_team_members')
#     else:
#         team_members = Register.objects.all()
#         form = TeamMembersAddForm()
#         return render(request, 'add_team_members.html', {'form': form, 'team': team, 'team_members': team_members})

def projectteammembersadd(request):
    if request.method == 'POST':
        form = ProjectTeamAddForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            team_members = form.cleaned_data['team_members']
            team = Team.objects.create(team_name=team_name)
            team.team_members.set(team_members)
            return redirect('/project_teammembers_view')
    else:
        form = ProjectTeamAddForm()
        return render(request, 'add_project_team_members.html', {'form': form})

def projectteammembersedit(request,id):
    data = Team.objects.get(id=id)
    form = ProjectTeamAddForm(request.POST,instance=data)
    if request.method=="POST":
        form.save()
        
        return redirect('/project_teammembers_view')
    else:
        form = ProjectTeamAddForm(instance=data)
    return render(request,'add_project_team_members.html',{'form':form})

def projectteammembersview(request):
    a = Team.objects.all()
    search = request.GET.get('search','')
    if search:
        a = a.filter(Q(team_name__icontains=search)|Q(team_members__name__icontains=search))
    return render(request,'view_team_project.html',{'a':a})
    
def projectteammembersdelete(request,id):
    a = Team.objects.get(id=id)
    a.delete()
    return redirect('/project_teammembers_view')

def projectteamedit(request, id):
    data = Team.objects.get(id=id)
    a = Projects.objects.filter(team=data)
    if request.method == "POST":
        form = ProjectTeamAddForm(request.POST, instance=data)
        if form.is_valid():
            initial_team_members = set(data.team_members.all())
            form.save()
            final_team_members = set(data.team_members.all())
            added_members = final_team_members - initial_team_members
            removed_members = initial_team_members - final_team_members
            for member in added_members:
                send_mail(
                    'You have been added to a project team',
                    'You have been added to the project team "{}".'.format(data.team_name),
                    settings.DEFAULT_FROM_EMAIL,
                    [member.email],
                    fail_silently=False,
                )
            for member in removed_members:
                send_mail(
                    'You have been removed from a project team',
                    'You have been removed from the project team "{}".'.format(data.team_name),
                    settings.DEFAULT_FROM_EMAIL,
                    [member.email],
                    fail_silently=False,
                )
            # project_history = ProjectHistory.objects.create(
            #     project=a,
            #     modified_by=request.user,
            #     modified_date=timezone.now(),
            #     old_team_name=data.team_name,
            #     new_team_name=form.cleaned_data['team_name'],
            #     team_members_add_status=1 if added_members else 0,
            #     team_members_delete_status=1 if removed_members else 0,
            # )
            return redirect('/view_project')

    else:
        form = ProjectTeamAddForm(instance=data)
    return render(request, 'add_project_team_members.html', {'form': form})



# def teammembersview(request):
#     a = Team_members.objects.all()
#     user_id = request.user.id
#     b = Team_members.objects.filter(team_members=user_id)
#     search = request.GET.get('search','')
#     if search:
#         a = a.filter(Q(team__team_name__icontains=search)|Q(team_members__name__icontains=search))
#         print(a)
#     return render(request,'view_team_members.html',{'a':a,'b':b})

# def teammembersedit(request,id):
#     data = Team_members.objects.get(id=id)
#     form=TeamMembersAddForm(request.POST,instance=data)
#     if request.method=='POST':
#         if form.is_valid():
#             data.save()
#             form.save()
#         return redirect('/view_team_members')
#     else:
#         form = TeamMembersAddForm(instance=data)
#         return render(request,'add_team_members.html',{'form':form})
    
# def teammembersprojectedit(request, id):
#     data = Team_members.objects.get(id=id)
#     form = TeamMembersAddForm(request.POST, instance=data)
#     if request.method == 'POST':
#         if form.is_valid():
#             data.save()
#             form.save()
#             return redirect('/view_project')
#     else:
#         form = TeamMembersAddForm(instance=data)
#     return render(request, 'add_team_members.html', {'form': form})

    
# def teammembersdelete(request,id):
#     data=Team_members.objects.get(id=id)
#     data.delete()
#     return redirect("/view_team_members")

# def teammembersdetailsview(request,id):
#     a = Team_members.objects.filter(id=id)
#     return render(request,'view_team_details.html',{'a':a})

# def teammemberview(request,id):
#     a = Team_members.objects.filter(projects=id)
#     b = Projects.objects.get(id=id)
#     print(b)
#     search = request.GET.get('search','')
#     if search:
#         a = a.filter(Q(team__team_name__icontains=search)|Q(team_members__name__icontains=search))
#         print(a)
#     return render(request,'view_teams.html',{'a':a,'b':b})