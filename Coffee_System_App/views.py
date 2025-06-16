from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

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

def costomer(request):
    return render(request, 'costomers.html')

def menu(request):
    return render(request, 'menus.html')

def order_detail(request):
    return render(request, 'order_details.html')

def order(request):
    return render(request, 'orders.html')

def payment(request):
    return render(request, 'payments.html')

def staff(request):
    return render(request, 'staffs.html')



# Create your views here.
