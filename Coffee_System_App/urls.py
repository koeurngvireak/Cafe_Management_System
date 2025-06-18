from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('logout/', views.logout_confirm, name='logout'),
    path('logout2/', views.logout_confirm2, name='logout2'),
    path('pos/index/', views.pos_system, name='pos-index'),
    
    
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

