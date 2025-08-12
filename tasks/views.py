from django.shortcuts import render

# Create your views here.


def manager_dashboard(request):

    return render(request, 'tasks/manager_dashboard.html', {})

def user_dashboard(request):
    return render(request, 'tasks/user_dashboard.html', {})