# from django.db import models

# # Create your models here.
# class drink(models.Model):
#     drink_id = models.AutoField(primary_key=True)
#     drink_name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     qty = models.IntegerField(default=0)
#     total_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
#     image = models.ImageField(upload_to='images/', default='images/default.jpg')
#     def __str__(self):
#         return self.drink_name
#     class customer(models.Model):
#         customer_N = models.AutoField(primary_key=True)
#         customer_id = models.CharField(max_length=10, unique=True)
#         total_drinks = models.IntegerField(default=0)
#         total_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
#         status = models.CharField(max_length=20, default='Pending')
#         def __str__(self):
#             return self.customer_id
        
#     class order_details(models.Model):
#         order_id = models.AutoField(primary_key=True)
#         drink = models.ForeignKey(drink, on_delete=models.CASCADE)
#         price = models.DecimalField(max_digits=5, decimal_places=2)
#         qty = models.IntegerField(default=1)
#         total = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

#         def __str__(self):
#             return f"Order {self.order_id} for {self.qty} x {self.drink.drink_name}"