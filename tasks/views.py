from django.shortcuts import render, redirect
from tasks.forms import TaskModelForm,TaskDetailModelForm
from tasks.models import Task,Project
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()
"""
@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):
    type = request.GET.get("type","all")
    
    counts = Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id',filter=Q(status='COMPLETED')),
        pending_task=Count('id',filter=Q(status='PENDING')),
        in_progress_task=Count('id',filter=Q(status='IN_PROGRESS')),
        
        
        )
    
    base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    
    if type == "completed":
        tasks = base_query.filter(status="COMPLETED")
        
    elif type == "in-progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == "pending":
        tasks = base_query.filter(status="PENDING")
    elif type == "all":
        tasks = base_query.all()
    
    context = {
        "tasks": tasks,
        "counts" : counts
    }
    return render(request,"dashboard/manager-dashboard.html", context)

"""


class ManagerDashboard(LoginRequiredMixin,UserPassesTestMixin,ListView):
    login_url = 'sign-in'
    template_name = 'dashboard/manager-dashboard.html'
    context_object_name = 'tasks'
    
    def test_func(self):
        return is_manager(self.request.user)
    def handle_no_permission(self):
        return redirect('no-permission')
    
    def get_queryset(self):
        type = self.request.GET.get("type","all")
        
        
        base_query = Task.objects.select_related("details").prefetch_related("assigned_to")
    
        if type == "completed":
            tasks = base_query.filter(status="COMPLETED")
            
        elif type == "in-progress":
            tasks = base_query.filter(status="IN_PROGRESS")
        elif type == "pending":
            tasks = base_query.filter(status="PENDING")
        elif type == "all":
            tasks = base_query.all()
        
        
        return tasks
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id',filter=Q(status='COMPLETED')),
        pending_task=Count('id',filter=Q(status='PENDING')),
        in_progress_task=Count('id',filter=Q(status='IN_PROGRESS')),
        )
            
        context['counts'] = counts
        return context
        
        
    





"""
@user_passes_test(is_employee,login_url='no-permission')
def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")
"""


class UserDashboard(View):
    
    def get(self,request,*args,**kwargs):
        return render(request,"dashboard/user-dashboard.html")

"""
def test(request):
    context = {
        "names": ["rakib","sakib","arif","john"],
        "age": [20,26,19]
    }
    return render(request,"test.html",context)
"""



# @login_required(login_url='sign-in')
# def create_task(request):
#     task_form = TaskModelForm()
#     task_detail_form = TaskDetailModelForm()
    
#     if request.method == "POST":
#         task_form = TaskModelForm(request.POST)
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
#         if task_form.is_valid() and task_detail_form.is_valid():
            
#             '''For Django Model Form'''
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
#             messages.success(request,"Task created successfully!")
#             return redirect('create-task')
                
                
#     context = {
#                 "task_form" : task_form,
#                 "task_detail_form" : task_detail_form
#             }
#     return render(request,"task_form.html",context)

# decorators = [login_required(login_url='sign-in'),permission_required('tasks.change_task',login_url='no-permission')]


class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """ For creating task """
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'task_form.html'

    """ 
    0. Create Task
    1. LoginRequiredMixin
    2. PermissionRequiredMixin
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get(
            'task_detail_form', TaskDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)


# class UpdateTask(View):
#     template_name = 'task_form.html'
#     def get(self,request,id, *args, **kwargs):
#         task = Task.objects.get(id=id)
#         task_form = TaskModelForm (instance = task)
#         if task.details:
#             task_detail_form = TaskDetailModelForm(instance = task.details)
#         context = {
#                 "task_form" : task_form,
#                 "task_detail_form" : task_detail_form
#             }
#         return render(request,self.template_name,context)

        
    
#     def post(self,request,id, *args, **kwargs):
#         task = Task.objects.get(id=id)
#         task_form = TaskModelForm(request.POST,instance = task)
#         task_detail_form = TaskDetailModelForm(request.POST,request.FILES,instance = task.details,)
#         if task_form.is_valid() and task_detail_form.is_valid():
            
#             '''For Django Model Form'''
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()
#             messages.success(request,"Task Updated successfully!")
#             return redirect('update-task', id)
        
        
        
"""
@login_required(login_url='sign-in')
@permission_required('tasks.change_task',login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm (instance = task)
    if task.details:
        task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance = task)
        task_detail_form = TaskDetailModelForm(request.POST,instance = task.details, type_enc="multipart")
        if task_form.is_valid() and task_detail_form.is_valid():
            
            '''For Django Model Form'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,"Task Updated successfully!")
            return redirect('update-task', id)
    
                
    context = {
                "task_form" : task_form,
                "task_detail_form" : task_detail_form
            }
    return render(request,"task_form.html",context)

"""


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance = self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()
        return context
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance = self.object)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=getattr(self.object, 'details', None))
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,"Task Updated successfully!")
            return redirect('update-task', self.object.id)
            







@login_required
@permission_required('tasks.delete_task',login_url='no-permission')
def delete_task(request,id):
    if request.method == 'POST':
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request,f"Task '{task.title}' deleted Successfully!")
        return redirect("manager-dashboard")
    else:
        messages.error(request,"Something went wrong")
        return redirect("manager-dashboard")
    
    
class DeleteTask(DeleteView):
    model = Task
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('dashboard')




# @login_required
# @permission_required('tasks.view_task',login_url='no-permission')
# def view_task(request):
#     tasks = Task.objects.prefetch_related('assigned_to').all()
#     task_count = Task.objects.aggregate(total = Count('id'))
#     projects = Project.objects.annotate(total_task = Count('tasks')).order_by('-total_task')
#     context = {
#         "tasks": tasks,
#         "task_count": task_count,
#         "projects": projects
#     }
#     return render(request,"show_task.html",context)

# @method_decorator(permission_required('projects.view_project',login_url='no-permission'), name='dispatch')
class View_Projrects(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Project
    template_name = 'show_task.html'
    context_object_name = 'projects'
    login_url = 'sign-in'
    permission_required = 'projects.view_projects'
    
    def get_queryset(self):
        return Project.objects.annotate(total_task = Count('tasks')).order_by('-total_task')


"""
@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def task_details(request,task_id):
    task = Task.objects.get(id = task_id)
    status_choices = Task.STATUS_CHOICES
    
    if request.method == "POST":
        status = request.POST.get("task_status")
        task.status = status
        task.save()
        return redirect("task-details",task_id)
    
    return render(request,"task_details.html",{"task":task, "status_choices":status_choices})
"""


class TaskDetails(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'
    login_url = 'sign-in'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args,**kwargs):
        task = self.get_object()
        status = request.POST.get("task_status")
        task.status = status
        task.save()
        return redirect("task-details",task.id)
    


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_manager(request.user):
        return redirect("manager-dashboard")
    elif is_employee(request.user):
        return redirect("user-dashboard")
    return redirect("no-permission")

