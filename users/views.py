from django.shortcuts import render, redirect


from .forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.

def sign_up(request):
    
    form = CustomRegistrationForm()

    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            

            form.save()
    
    context = {
        "form":form
    }
    return render(request, 'users/registration/register.html',context)

def sign_in(request):

    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render (request, 'users/registration/signIn.html')

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')