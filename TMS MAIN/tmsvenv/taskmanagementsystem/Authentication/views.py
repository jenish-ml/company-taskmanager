from django.shortcuts import render,redirect
from .forms import *
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')



def dologin(request):
    form = LoginForm()
    if request.method == "POST":
        user = authenticate(request,username=request.POST["username"],password=request.POST["password"] )
        if user is None:
            return render(request,'index.html',{'a':True})
        else:
            login(request, user)
            data = Register.objects.get(username=user.username)
            request.session['ut']=data.usertype
            data.usertype
            request.session['userid']=data.id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

def dologout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/login')
def staffadd(request):
    if request.user.usertype != 1:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = StaffAddForm(request.POST, request.FILES)
        try:
            Register.objects.get(username=request.POST['email'])
            return render(request,'add_staff.html',{'form':form,'x':True})
        except Register.DoesNotExist:
            if form.is_valid():
                designation = form.cleaned_data['designation']
                username = form.cleaned_data['email']
                password=form.cleaned_data['password']
                email=form.cleaned_data['email']
                related_designation=designation.role.lower()
                if related_designation == "manager":
                    usertype = 2
                else:
                    usertype = 3
                Register.objects.create_user(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=password,
                contact=form.cleaned_data['contact'],
                designation=designation,
                username=username,
                usertype=usertype 
                )
                send_mail(
                    subject="Task Management System Register",
                    message="You are registered By Admin . Your Password Is " + str(password) + " Your Designation is " + str(designation),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                )
                return redirect('/view_staff')
    else:
        form = StaffAddForm()
    return render(request, 'add_staff.html', {'form': form})

@login_required(login_url='/login')
def staffview(request):
    if request.user.usertype != 1:
        return render(request, 'access_denied.html')
    a = Register.objects.exclude(usertype="1")
    search = request.GET.get('search','')
    if search:
        a = a.filter(Q(name__icontains=search)|Q(designation__role__icontains=search)|Q(email__icontains=search))
        print(a)
    return render(request,'view_staff.html',{'a':a})

@login_required(login_url='/login')
def staffedit(request, id):
    data = Register.objects.get(id=id)
    if request.user.usertype != 1:
        return render(request, 'access_denied.html')
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=data)    
        if form.is_valid():
            related_designation = data.designation.role.lower()
            print(related_designation)
            email = form.cleaned_data['email']
            if related_designation == "manager":
                data.usertype = 2
            else:
                data.usertype = 3
            data.save()
            form.save()
            send_mail(
                subject="Task Management System",
                message="Your designation will be changed to "+ str(related_designation),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            return redirect('/view_staff')
    else:
        form = StaffEditForm(instance=data)
    return render(request, 'Edit_staff.html', {'form': form})

@login_required(login_url='/login')
def staffdelete(request,id):
    data=Register.objects.get(id=id)
    data.delete()
    return redirect('/view_staff')
        