from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', views.logout_confirm, name='logout'),
    path('pos/', views.pos_system, name='pos'),
    path('custom_redirect/', views.custom_redirect, name='custom_redirect'),
    path('home/', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('inventory/', views.inventory, name='inventory'),
    path('customers/', views.customers, name='customers'),
    path('settings/', views.settings, name='settings'),
   
    
]

