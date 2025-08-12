from django.urls import path

from .views import manager_dashboard, user_dashboard, create_task, view_task

urlpatterns = [
    path('manager-dashboard/',manager_dashboard, name='manager-dashboard' ),
    path('user-dashboard/',user_dashboard ),
    path('create-task/', create_task),
    path('view-task/', view_task),
]