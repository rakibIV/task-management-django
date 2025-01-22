from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

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
    tasks = Task.objects.all()
    task_3 = Task.objects.get(id=3)
    context = {
        "tasks": tasks,
        "task3" : task_3
    }
    return render(request,"show_task.html",context)