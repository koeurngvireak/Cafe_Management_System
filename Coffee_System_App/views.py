from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomLoginForm
from django.views.decorators.cache import never_cache



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('home')        # Admin
            else:
                return redirect('pos-index')   # Normal user

        else:
            return render(request, 'login/Login.html', {'error': 'Invalid credentials'})

    return render(request, 'login/Login.html')

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login/logout.html')

def logout_confirm2(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'pos/logout2.html')
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@user_passes_test(lambda u: not u.is_staff)
def pos_system(request):
    return render(request, 'pos/index.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def feature(request):
    return render(request, 'feature.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    return render(request, 'overview.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def orders(request):
    return render(request, 'accept_order.html')
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def inventory(request):
    return render(request, 'pending.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def customers(request):
    return render(request, 'update_drink.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def settings(request):
    return render(request, 'cheach_history.html')








# Create your views here.
