from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Sum,Max,Min,Avg
from django.contrib import messages

# Create your views here.



def manager_dashboard(request):
    type = request.GET.get("type","all")
    
    # total_task = tasks.count()
    # completed_task = tasks.filter(status="COMPLETED").count()
    # pending_task = tasks.filter(status="PENDING").count()
    # in_progress_task = tasks.filter(status="IN_PROGRESS").count()
    
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


def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")


def test(request):
    context = {
        "names": ["rakib","sakib","arif","john"],
        "age": [20,26,19]
    }
    return render(request,"test.html",context)


def create_task(request):
    # employees = Employee.objects.all()
    # form = TaskForm(employees=employees)
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            '''For Django Model Form'''
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request,"Task created successfully!")
            return redirect('create-task')
            
            
            
            '''For Django Form'''
            
            # data = form.cleaned_data
            # title = data.get("title")
            # description = data.get("description")
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to")
            
            # task = Task.objects.create(
            #     title = title,
            #     description = description,
            #     due_date = due_date,
            # )
            
            # # Assign employee to task
            # for emp_id in assigned_to:
            #     task.assigned_to.add(emp_id)
                
                
    context = {
                "task_form" : task_form,
                "task_detail_form" : task_detail_form
            }
    return render(request,"task_form.html",context)


def update_task(request, id):
    task = Task.objects.get(id = id)
    task_form = TaskModelForm (instance = task)
    if task.details:
        task_detail_form = TaskDetailModelForm(instance = task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST,instance = task)
        task_detail_form = TaskDetailModelForm(request.POST,instance = task.details)
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


def delete_task(request,id):
    if request.method == 'POST':
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request,f"Task '{task.title}' deleted Successfully!")
        return redirect("manager-dashboard")
    else:
        messages.error(request,"Something went wrong")
        return redirect("manager-dashboard")





def view_task(request):
    # tasks = Task.objects.filter(title__icontains="p", status="PENDING")
    # tasks = Task.objects.select_related("details").all()
    # tasks = TaskDetail.objects.select_related("task").all()
    # tasks = Task.objects.select_related("projects").all()
    # tasks = Project.objects.prefetch_related('tasks').all()
    tasks = Task.objects.prefetch_related('assigned_to').all()
    task_count = Task.objects.aggregate(total = Count('id'))
    projects = Project.objects.annotate(total_task = Count('tasks')).order_by('-total_task')
    context = {
        "tasks": tasks,
        "task_count": task_count,
        "projects": projects
    }
    return render(request,"show_task.html",context)

