from django.urls import path
from . import views
from .views import StaffLoginView, StaffLogoutView

urlpatterns = [
    # Authentication URLs
    path('', StaffLoginView.as_view(), name='staff_login'),
    path('logout/', StaffLogoutView.as_view(), name='staff_logout'),

    # Main Application URLs
    path('overview/', views.overview, name='overview'),
    path('feature/',views.feature, name='feature'), # Feature page
    path('home/', views.home, name='home'),# Home page / Overview
    path('pos/', views.pos_system, name='pos_system'),
    path('pos/process_order/', views.process_order, name='process_order'),

    path('accept_order/', views.accept_order, name='accept_order'),
    path('api/order_details/<int:order_id>/', views.get_order_details, name='api_order_details'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order_view, name='cancel_order'),

    path('pending_orders/', views.pending_orders_view, name='pending_orders'),
    path('mark_completed/<int:order_id>/', views.mark_order_completed, name='mark_order_completed'),

    path('update_drink/', views.update_drink, name='update_drink'),
    path('delete_drink/<int:drink_id>/', views.delete_drink, name='delete_drink'),

    # Static Pages (adjust templates as needed)
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('history/', views.cheach_history, name='cheach_history'),
]