from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User, Group
from users.forms import RegisterForm,CustomRegistrationForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    form = CustomRegistrationForm()
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request,"A confirmation mail sent. Please check your email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
    context = {
        "form":form
    }
    return render(request,'registration/register.html',context)


def sign_in(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("doc:",username,password)
        
        user = authenticate(request,username=username,password=password)
        print("user:",user)
        
        if user:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,"Username or password is incorrect")
        
    return render(request,'registration/login.html', {})


@login_required(login_url='sign-in')
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    
    
def activate_user(request,user_id,token):
    user = User.objects.get(id=user_id)
    try :
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request,"Your account is activated. Please login")
            return redirect('sign-in')
        else :
            messages.error(request,"Invalid token")
            return redirect('sign-in')
    except Exception as e:
        messages.error(request,"Invalid token")
        return redirect('sign-in')

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No group assigned"
    context = {
        "users":users
    }
    return render(request,'admin/dashboard.html',context)

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            print("role:",role)
            print("user:",user)
            user.groups.clear()
            user.groups.add(role)
            # messages.success(request,"Role assigned successfully")
            return redirect('admin-dashboard')
        
    return render(request,'admin/assign_role.html',{"form":form})
@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,"Group created successfully")
            return redirect('admin-dashboard')
        
    return render(request,'admin/create_group.html',{"form":form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    context = {
        "groups":groups
    }
    
    return render(request,'admin/group_list.html',context)