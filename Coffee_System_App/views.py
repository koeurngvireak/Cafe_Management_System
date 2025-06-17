from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

# Login page
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:  # Admin
                return redirect("home.html")
            else:  # Regular user
                return redirect("pos")
        else:
            return render(request, "login/login.html", {"error": "Invalid credentials"})
    return render(request, "login/login.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, "home.html")
    return redirect("pos")

@login_required(login_url="login")
def user_home(request):
    return render(request, "pos/index.html")

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login/logout.html')

def base(request):
    return render(request, 'base.html')

def feature(request):
    return render(request, 'feature.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request, 'overview.html')

def orders(request):
    return render(request, 'accept_order.html')

def inventory(request):
    return render(request, 'pending.html')

def customers(request):
    return render(request, 'update_drink.html')

def settings(request):
    return render(request, 'cheach_history.html')

def pos_system(request):
    return render(request, 'pos/index.html')



# Create your views here.
