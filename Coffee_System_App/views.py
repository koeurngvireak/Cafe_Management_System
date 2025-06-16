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

def customer(request):
    return render(request, 'Customers/customers.html')

def menu(request):
    return render(request, 'Menu_Items/menus.html')

def order_detail(request):
    return render(request, 'Order_Details/order_details.html')

def order(request):
    return render(request, 'Orders/orders.html')

def payment(request):
    return render(request, 'Payments/payments.html')

def add_user(request):
    return render(request, 'Add_Users/add_users.html')



# Create your views here.
