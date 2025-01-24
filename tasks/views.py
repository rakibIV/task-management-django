from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Sum,Max,Min,Avg

# Create your views here.



def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")


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
    form = TaskModelForm()
    
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            
            '''For Django Model Form'''
            form.save()
            return render(request,"task_form.html",{"form":form, "message": "Task Created Successfully"})
            
            
            
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
        "form": form
    }
    return render(request,"task_form.html",context)




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