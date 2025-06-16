from django.urls import path
from . import views 

app_name = 'Coffee_System_App'

urlpatterns = [
    path('', views.base, name='layout'),
    path('costomers/', views.costomer, name='costomers'),
    path('menus/', views.menu, name='menus'),
    path('orders/', views.order, name='orders'),
    path('payments/', views.payment, name='payments'),
    path('staffs/', views.staff, name='staffs'),
]

