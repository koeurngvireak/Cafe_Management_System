from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feature/', views.feature, name='feature'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('customer/', views.customer, name='customer'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('payment/', views.payment, name='payment'),
    path('add_user/', views.add_user, name='add_user'),
    path('order_detail/', views.order_detail, name='order_detail'),
]

