from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Drink, Order, OrderItem, Customer

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'hot_price', 'iced_price', 'frappe_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drink Name'}),
            'hot_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hot Price (optional)'}),
            'iced_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Iced Price (optional)'}),
            'frappe_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Frappe Price (optional)'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['drink', 'quantity']
        widgets = {
            'drink': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

# You might need a form for adding/editing a customer, especially for accept_order
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email'] # customer_id might be auto-generated or based on something unique
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)