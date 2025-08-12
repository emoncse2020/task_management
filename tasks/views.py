from django.shortcuts import render
from .forms import TaskModelForm
from .models import Task, TaskDetail, Employee, Project

# Create your views here.


def manager_dashboard(request):

    return render(request, 'tasks/manager_dashboard.html', {})

def user_dashboard(request):
    return render(request, 'tasks/user_dashboard.html', {})


def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()  # For GET

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """ For Model Form Data """
            form.save()

            return render(request, 'task_form.html', {"form": form, "message": "task added successfully"})

    context = {"form": form}
    return render(request, "tasks/task_form.html", context)

def view_task(request):
    tasks = Task.objects.all()

    # select_related(ForeignKey, OneToOneField)
    # tasks = Task.objects.select_related('details').all()
    tasks = TaskDetail.objects.select_related('task').all()
    context = {
        "tasks" : tasks
    }
    return render (request, 'tasks/show_task.html', context)