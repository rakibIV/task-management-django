from django.urls import path
from tasks.views import ManagerDashboard, UserDashboard,DeleteTask,dashboard,CreateTask,View_Projrects,TaskDetails, UpdateTask

urlpatterns = [
    path('manager/', ManagerDashboard.as_view(), name='manager-dashboard'),
    path('user/', UserDashboard.as_view(), name='user-dashboard'),
    # path('create-task/', create_task, name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    # path('view-task/', view_task, name = 'view-task'),
    path('view-projects/', View_Projrects.as_view(), name = 'view-projects'),
    # path("task/<int:task_id>/details", task_details, name="task-details"),
    path("task/<int:task_id>/details", TaskDetails.as_view(), name="task-details"),
    # path("update-task/<int:id>/",update_task, name="update-task"),
    path("update-task/<int:id>/",UpdateTask.as_view(), name="update-task"),
    path("delete-task/<int:id>/",DeleteTask.as_view(), name="delete-task"),
    path("dashboard/",dashboard, name="dashboard"),
    
]