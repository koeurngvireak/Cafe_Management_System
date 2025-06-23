from django.contrib import admin
from .models import Drink, Customer, Order, OrderItem
from django.utils.html import format_html # Import format_html

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'hot_price', 'iced_price', 'frappe_price', 'is_available', 'image_tag')
    list_filter = ('is_available',)
    search_fields = ('name',)
    readonly_fields = ('image_tag',) # Make image_tag readonly

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image' # Column header in admin

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'phone_number', 'email')
    search_fields = ('customer_id', 'name', 'phone_number', 'email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Don't show extra empty forms

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'total_drinks', 'total_price', 'status', 'staff')
    list_filter = ('status', 'order_date', 'staff')
    search_fields = ('customer__name', 'customer__customer_id', 'id')
    inlines = [OrderItemInline]
    date_hierarchy = 'order_date'
    raw_id_fields = ('customer', 'staff')