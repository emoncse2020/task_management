from django.shortcuts import render, redirect
from .forms import TaskModelForm, TaskDetailModelForm
from .models import Task, TaskDetail
from django.db.models import Count,Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from users.views import is_admin

from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import DetailView,UpdateView
# Create your views here.

# variable for list of decoratiors



def is_manager(user):
    return user.groups.filter(name="Manager").exists()
def is_employee(user):
    return user.groups.filter(name="Employee").exists()

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    counts = Task.objects.aggregate(
        total =Count('id'),
        completed =Count('id', filter=Q(status='COMPLETED')),
        in_progress =Count('id', filter=Q(status='IN_PROGRESS')),
        pending =Count('id', filter=Q(status='PENDING')),               
                         )
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')


    type = request.GET.get('type', 'all')     

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')   

    elif type == "in_progress":
        tasks = base_query.filter(status ="IN_PROGRESS")   

    elif type == "pending":
        tasks = base_query.filter(status ="PENDING")   

    elif type == 'all':
        tasks = base_query.all()

    



    context = {
        "tasks" : tasks,
        "counts": counts
        
    }

    return render(request, 'tasks/manager_dashboard.html', context)


@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, 'tasks/employee_dashboard.html', {})

# @login_required
# @permission_required('tasks.add_task', login_url='no-permission')
# def create_task(request):
#     # employees = Employee.objects.all()
#     task_form = TaskModelForm()  # For GET
#     task_detail_form = TaskDetailModelForm()


#     if request.method == "POST":
#         task_form = TaskModelForm(request.POST)  
#         task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
#         if task_form.is_valid() and task_detail_form.is_valid():

#             """ For Model Form Data """
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task
#             task_detail.save()


#             messages.success(request, "Task  Created Successfully.")
#             return redirect('create-task')

#     context = {"task_form":task_form, "task_detail_form":task_detail_form}
#     return render(request, "tasks/task_form.html", context)


class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'

    """For creating task """
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
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


            messages.success(request, "Task  Created Successfully.")
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)


@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    # employees = Employee.objects.all()
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)


    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task )  
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task  Updated Successfully.")
            return redirect('update-task', id)

    context = {"task_form":task_form, "task_detail_form":task_detail_form}
    return render(request, "tasks/task_form.html", context)

class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'tasks/task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['task_form'] = self.get_form() 

        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_detail_form = TaskDetailModelForm(request.POST, instance=getattr(self.object, 'details', None))
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task  Updated Successfully.")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)

# delete task
@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    if request.method=="POST":
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task delete successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request, "Something went wrong")
        return redirect('manager-dashboard')
    
@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    tasks = Task.objects.all()

    # select_related(ForeignKey, OneToOneField)
    # tasks = Task.objects.select_related('details').all()
    tasks = TaskDetail.objects.select_related('task').all()
    context = {
        "tasks" : tasks
    }
    return render (request, 'tasks/show_task.html', context)

# @login_required
# @permission_required('tasks.view_task', login_url='no-permission')
# def task_details(request, id):

#     task = Task.objects.get(id=id)
#     status_choices = Task.STATUS_CHOICES

#     if request.method == "POST":
#         selected_status = request.POST.get('task_status')
#         task.status = selected_status
#         task.save()
#         return redirect('task-details', task.id)

#     context = {
#         "task":task,
#         'status_choices':status_choices
#     }
#     return render(request, 'tasks/task_details.html', context)

class TaskDetails(DetailView):
    model = Task
    template_name = 'tasks/task_details.html'
    context_object_name = 'task'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.pk)


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    
    elif is_employee(request.user):
        return redirect('user-dashboard')
    
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    return redirect('no-permission')