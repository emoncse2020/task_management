from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def no_permission(request):
    return render(request, 'core/no_permission.html')