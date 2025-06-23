from django.db import models
from django.conf import settings # To link to Django's built-in User model

class Drink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='drinks/', blank=True, null=True) # Images stored in media/drinks/
    hot_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    iced_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    frappe_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True) # To easily "drop" a drink from the menu

    def __str__(self):
        return self.name

class Customer(models.Model):
    # If you want more detailed customer info, add fields here
    customer_id = models.CharField(max_length=50, unique=True) # You might use a UUID or auto-incrementing ID later
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else self.customer_id

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True) # Orders can be anonymous
    order_date = models.DateTimeField(auto_now_add=True)
    total_drinks = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # You might want to link the staff who made the order
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT) # Don't delete drink if part of an order
    price_at_order = models.DecimalField(max_digits=6, decimal_places=2) # Price when order was made
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.subtotal = self.price_at_order * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.drink.name} for Order {self.order.id}"