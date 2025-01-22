from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, test, create_task,view_task

urlpatterns = [
    path('manager/', manager_dashboard),
    path('user/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task),
    path('view_task/', view_task),
    
]