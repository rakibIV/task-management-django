from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm

# Create your views here.

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
        
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password1 = form.cleaned_data.get('password1')
            # password2 = form.cleaned_data.get('password2')
            # if password1 == password2:
            #     User.objects.create(username=username,password=password1)
            # else:
            #     print("passwords are not matched")   
            form.save()
        else:
            print("Form is not valid")
    context = {
        "form":form
    }
    return render(request,'registration/register.html',context)
