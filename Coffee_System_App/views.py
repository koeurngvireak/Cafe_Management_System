from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Set session expiry based on remember me
            if not remember:
                request.session.set_expiry(0)
            
            # Get next URL from query parameters or use default
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('pos')  # Change 'dashboard' to your default redirect URL
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login/login.html')
@login_required
def custom_redirect(request):
    if request.user.is_superuser:
        return render(request, 'home')
    else:
        return redirect('pos')
def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login/logout.html')

def base(request):
    return render(request, 'base.html')
def home(request):
    return render(request, 'home.html')

def feature(request):
    return render(request, 'feature.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def orders(request):
    return render(request, 'orders.html')

def inventory(request):
    return render(request, 'inventory.html')

def customers(request):
    return render(request, 'customers.html')

def settings(request):
    return render(request, 'settings.html')

def pos_system(request):
    return render(request, 'pos/index.html')



# Create your views here.
