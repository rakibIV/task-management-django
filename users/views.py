from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def sign_up(request):
    form = CustomRegistrationForm()
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"User has been created successfully") 
            form.save()
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



def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
