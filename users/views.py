from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm

# Create your views here.

def sign_up(request):
    if request.method == "GET":
        form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            # form_data = form.cleaned_data
            # username = form_data.get('username')
            # password = form_data.get('password1')
            # confirm_password = form_data.get('password2')

            # if password == confirm_password:
            #     User.objects.create(username=username, password=password)

            # else:
            #     print("password are not same")

            form.save()
    
    context = {
        "form":form
    }
    return render(request, 'users/registration/register.html',context)