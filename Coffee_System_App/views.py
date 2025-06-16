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

# Create your views here.
