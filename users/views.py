from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import Group
from users.forms import RegisterForm,CustomRegistrationForm, AssignRoleForm, CreateGroupForm, PassChangeForm,PassResetForm,PassResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

User = get_user_model()
# Create your views here.

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()
"""
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
"""
class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        user = form.save(commit=False)  
        if form.cleaned_data['password1'] != form.cleaned_data['confirm_password']:
            return self.form_invalid(form)
        user.set_password(form.cleaned_data['password1'])  
        user.save()
        messages.success(self.request, "A confirmation email has been sent. Please check your email.")
        return super().form_valid(form)
    
    

"""
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
            print("user not found")
            messages.error(request,"Username or password is incorrect")
            
        
    return render(request,'registration/login.html', {})
    
"""




class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def post(self, request, *args, **kwargs):
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("doc:", username, password)  

        user = authenticate(request, username=username, password=password)
        print("user:", user) 

        if user:
           
            login(request, user)
            # messages.success(request, "Welcome back! You've successfully logged in.")
            return redirect('home')  
        else:
            messages.error(request, "Username or password is incorrect.")
            return render(request, self.template_name)


    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    
    

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/pass_change.html'
    form_class = PassChangeForm
    
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/pass_reset.html'
    form_class = PassResetForm
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context    
    def form_valid(self, form):
        messages.success(self.request, "Password reset email sent. Please check your email.")
        return super().form_valid(form)
    
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/pass_reset.html'
    form_class = PassResetConfirmForm
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        messages.success(self.request, "Password reset Successfully!")
        return super().form_valid(form)
    


"""
@login_required(login_url='sign-in')
def sign_out(request):
    if request.method == "POST":
        print("logging out from function based view")
        logout(request)
        return redirect('home')
    
"""

    

    
    
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

"""
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
    return render(request,'admin/admin_dashboard.html',context)
"""


class AdminDashboard(LoginRequiredMixin,UserPassesTestMixin,TemplateView):
    login_url = 'sign-in'
    template_name = 'admin/admin_dashboard.html'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = "No group assigned"
        context['users'] = users
        return context



"""
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
"""



class AssignRole(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = 'sign-in'
    model = User
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    context_object_name = 'form'
    pk_url_kwarg = 'id'
    
    def test_func(self):
        return is_admin(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.get(id=user_id)
        context['user'] = user
        return context
    
    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        user = self.get_object()
        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request,"Role assigned successfully")
        return redirect('admin-dashboard')

"""
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
"""



class CreateGroup(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('admin-dashboard')
    
    def test_func(self):
        return is_admin(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')
        

"""
@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    context = {
        "groups":groups
    }
    
    return render(request,'admin/group_list.html',context)
"""




class GroupList(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    
    def get_queryset(self):
        return Group.objects.prefetch_related("permissions").all()

