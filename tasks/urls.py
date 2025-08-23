from django.urls import path

from .views import manager_dashboard, employee_dashboard, view_task, update_task, delete_task, dashboard, CreateTask, TaskDetails, UpdateTask

urlpatterns = [
    path('manager-dashboard/',manager_dashboard, name='manager-dashboard' ),
    path('employee-dashboard/',employee_dashboard, name='user-dashboard' ),
    # path('create-task/', create_task, name='create-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('view-task/', view_task),
    path('update-task/<int:id>/',UpdateTask.as_view(), name='update-task'),
    # path('update-task/<int:id>/',update_task, name='update-task'),
    path('delete-task/<int:id>/',delete_task, name='delete-task'),
    # path('task/<int:id>/details/', task_details, name='task-details'),
    path('task/<int:pk>/details/', TaskDetails.as_view(), name='task-details'),
    path('dashboard/', dashboard, name='dashboard')
]