from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('costomers/', views.costomer, name='costomers'),
    path('menus/', views.menu, name='menus'),
    path('orders/', views.order, name='orders'),
    path('payments/', views.payment, name='payments'),
    path('staffs/', views.staff, name='staffs'),
]

