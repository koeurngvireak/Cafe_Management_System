from django.http import HttpResponse
from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

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
