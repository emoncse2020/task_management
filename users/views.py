from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import CustomRegistrationForm, CreateGroupForm
from django.contrib.auth import login,  logout
from .forms import LoginForm, AssignRoleForm
from django.contrib.auth.tokens import default_token_generator
# Create your views here.
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test

# test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            

            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, 'A confirmation main sent. Please check your email')
            return redirect('sign-in')
    
    context = {
        "form":form
    }
    return render(request, 'users/registration/register.html',context)

def sign_in(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    context = {
        "form": form
    }
    return render (request, 'users/registration/signIn.html',context )

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
        
    except User.DoesNotExist:
        return HttpResponse("user does not exist")

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"
    context = {
        "users":users
    }
    return render(request, 'users/admin/user_list.html', context)

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    form = AssignRoleForm()
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')
        
    context = {
        "form" : form
    }
    
    return render(request, 'users/admin/assign_role.html', context)

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect ('create-group')
        
    context = {
        "form" : form

    }
        
    return render(request, 'users/admin/create_group.html', context)

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    context = {
        "groups": groups
    }
    return render (request, 'users/admin/group_list.html', context)