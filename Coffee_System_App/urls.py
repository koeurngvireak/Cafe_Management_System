from django.urls import path
from . import views 

app_name = 'Coffee_System_App'

urlpatterns = [
    path('', views.layout, name='layout'),
    
]

