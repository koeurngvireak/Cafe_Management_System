from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db import transaction
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Drink, Order, OrderItem, Customer
from .forms import DrinkForm, OrderItemForm, CustomerForm

# --- Authentication ---
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class StaffLoginView(LoginView):
    template_name = 'login/Login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('overview')

class StaffLogoutView(LogoutView):
    next_page = reverse_lazy('staff_login')
    
@login_required
def home(request):
    return render(request, 'home.html')

# --- Overview View ---
@login_required
def overview(request):
    current_tz = timezone.get_current_timezone()
    today = timezone.localdate()
    start_of_day = datetime.combine(today, datetime.min.time(), tzinfo=current_tz)
    end_of_day = datetime.combine(today, datetime.max.time(), tzinfo=current_tz)

    daily_sales = Order.objects.filter(
        order_date__range=(start_of_day, end_of_day),
        status__in=['accepted', 'completed']
    ).aggregate(total_earnings=Sum('total_price'), total_orders=Count('id'))

    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    start_of_month_dt = datetime.combine(start_of_month, datetime.min.time(), tzinfo=current_tz)
    end_of_month_dt = datetime.combine(end_of_month, datetime.max.time(), tzinfo=current_tz)

    monthly_sales = Order.objects.filter(
        order_date__range=(start_of_month_dt, end_of_month_dt),
        status__in=['accepted', 'completed']
    ).aggregate(total_earnings=Sum('total_price'), total_orders=Count('id'))

    all_time_sales = Order.objects.filter(
        status__in=['accepted', 'completed']
    ).aggregate(total_earnings=Sum('total_price'), total_orders=Count('id'))

    total_customers = Customer.objects.count()

    sales_data_7_days = []
    dates = []
    for i in range(7):
        date = today - timedelta(days=i)
        start = datetime.combine(date, datetime.min.time(), tzinfo=current_tz)
        end = datetime.combine(date, datetime.max.time(), tzinfo=current_tz)
        day_sales = Order.objects.filter(
            order_date__range=(start, end),
            status__in=['accepted', 'completed']
        ).aggregate(total=Sum('total_price'))['total'] or 0.00

        sales_data_7_days.append(float(day_sales))
        dates.append(date.strftime('%Y-%m-%d'))

    sales_data_7_days.reverse()
    dates.reverse()

    context = {
        'daily_earnings': daily_sales['total_earnings'] or 0.00,
        'daily_orders': daily_sales['total_orders'] or 0,
        'monthly_earnings': monthly_sales['total_earnings'] or 0.00,
        'monthly_orders': monthly_sales['total_orders'] or 0,
        'all_time_earnings': all_time_sales['total_earnings'] or 0.00,
        'all_time_orders': all_time_sales['total_orders'] or 0,
        'total_customers': total_customers,
        'chart_labels': dates,
        'chart_data': sales_data_7_days,
    }
    return render(request, 'overview.html', context)

# --- POS System (index.html) ---
@login_required
def pos_system(request):
    drinks = Drink.objects.filter(is_available=True)
    context = {
        'drinks': drinks,
    }
    return render(request, 'pos/index.html', context)

@login_required
@transaction.atomic
def process_order(request):
    if request.method == 'POST':
        import json
        try:
            items_json_list = request.POST.getlist('items[]')
            order_items_data = [json.loads(item_str) for item_str in items_json_list]
        except (json.JSONDecodeError, TypeError) as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid order items data: {e}'}, status=400)

        # --- Handle Customer ---
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')

        customer = None
        if customer_name or customer_phone:
            if customer_phone:
                customer, created = Customer.objects.get_or_create(
                    phone_number=customer_phone,
                    defaults={'name': customer_name or f'Anonymous-{customer_phone}',
                              'customer_id': f"CUST-{int(datetime.now().timestamp())}"}
                )
                if not created and customer_name and customer.name != customer_name:
                    customer.name = customer_name
                    customer.save()
            elif customer_name:
                 customer, created = Customer.objects.get_or_create(
                    name=customer_name, # Note: This might create duplicates if names aren't unique and no phone
                    defaults={'customer_id': f"CUST-{int(datetime.now().timestamp())}"}
                 )

        # --- Create Order ---
        try:
            total_drinks = int(request.POST.get('total_drinks', 0))
            total_price = float(request.POST.get('total_price', 0.00))
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid total drinks or total price.'}, status=400)


        order = Order.objects.create(
            customer=customer,
            total_drinks=total_drinks,
            total_price=total_price,
            status='pending',
            staff=request.user
        )

        # --- Create Order Items ---
        for item_data in order_items_data:
            try:
                drink = get_object_or_404(Drink, id=item_data['drink_id'])
                OrderItem.objects.create(
                    order=order,
                    drink=drink,
                    quantity=int(item_data['quantity']),
                    price_at_order=float(item_data['price_at_order'])
                )
            except (KeyError, ValueError) as e:
                transaction.set_rollback(True)
                return JsonResponse({'status': 'error', 'message': f'Invalid item data for drink {item_data.get("drink_id")}: {e}'}, status=400)
            except Drink.DoesNotExist:
                transaction.set_rollback(True)
                return JsonResponse({'status': 'error', 'message': f'Drink with ID {item_data.get("drink_id")} not found.'}, status=400)

        return JsonResponse({'status': 'success', 'order_id': order.id, 'message': 'Order created successfully. Please confirm in Accept Order.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# --- Accept Order View ---
@login_required
def accept_order(request):
    pending_orders = Order.objects.filter(status='pending').order_by('-order_date')
    context = {
        'pending_orders': pending_orders,
    }
    return render(request, 'accept_order.html', context)

@login_required
def get_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    customer_info = {}
    if order.customer:
        customer_info = {
            'id': order.customer.customer_id,
            'name': order.customer.name,
            'phone': order.customer.phone_number,
        }

    items_data = []
    for item in order_items:
        items_data.append({
            'drink_name': item.drink.name,
            'price': float(item.price_at_order),
            'quantity': item.quantity,
            'subtotal': float(item.subtotal)
        })

    order_data = {
        'id': order.id,
        'customer': customer_info,
        'total_drinks': order.total_drinks,
        'total_price': float(order.total_price),
        'status': order.status,
        'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'items': items_data,
        'staff': order.staff.username if order.staff else 'N/A' # Include staff username
    }
    return JsonResponse(order_data)


@login_required
@transaction.atomic
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'pending':
        order.status = 'accepted'
        order.save()
        return JsonResponse({'status': 'success', 'message': f'Order {order_id} confirmed.'})
    return JsonResponse({'status': 'error', 'message': f'Order {order_id} cannot be confirmed.'}, status=400)

@login_required
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status in ['pending', 'accepted']:
        order.status = 'cancelled'
        order.save()
        return JsonResponse({'status': 'success', 'message': f'Order {order_id} cancelled.'})
    return JsonResponse({'status': 'error', 'message': f'Order {order_id} cannot be cancelled.'}, status=400)


# --- Pending Order View ---
@login_required
def pending_orders_view(request):
    orders = Order.objects.filter(status__in=['pending', 'accepted']).order_by('-order_date')
    context = {
        'orders': orders,
    }
    return render(request, 'pending.html', context)

@login_required
def mark_order_completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'accepted':
        order.status = 'completed'
        order.save()
        return JsonResponse({'status': 'success', 'message': f'Order {order_id} marked as completed.'})
    return JsonResponse({'status': 'error', 'message': f'Order {order_id} cannot be marked completed.'}, status=400)


# --- Update Drink View ---
@login_required
def update_drink(request):
    drinks = Drink.objects.filter(is_available=True).order_by('name')
    form = DrinkForm()
    editing_drink_id = None

    if request.method == 'POST':
        drink_id = request.POST.get('drink_id')
        if drink_id: # Updating existing drink
            drink_instance = get_object_or_404(Drink, id=drink_id)
            form = DrinkForm(request.POST, request.FILES, instance=drink_instance) # Pass request.FILES for image
            editing_drink_id = drink_id # Keep track of which drink was being edited for re-rendering form
        else: # Adding new drink
            form = DrinkForm(request.POST, request.FILES) # Pass request.FILES for image

        if form.is_valid():
            form.save()
            return redirect('update_drink') # Redirect to clear form and show updated list
        else:
            # If form is not valid, re-render with errors
            context = {
                'drinks': drinks,
                'form': form,
                'editing_drink_id': editing_drink_id # To pre-fill form if editing failed
            }
            return render(request, 'update_drink.html', context)

    context = {
        'drinks': drinks,
        'form': form,
        'editing_drink_id': editing_drink_id,
    }
    return render(request, 'update_drink.html', context)

@login_required
def delete_drink(request, drink_id):
    drink = get_object_or_404(Drink, id=drink_id)
    # Instead of truly deleting, we mark it as unavailable
    # This prevents issues if the drink is part of past orders.
    drink.is_available = False
    drink.save()
    return JsonResponse({'status': 'success', 'message': f'Drink "{drink.name}" has been dropped.'})

# --- Other Views ---
@login_required
def contact(request):
    return render(request, 'contact.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def cheach_history(request):
    orders = Order.objects.filter(status__in=['accepted', 'completed', 'cancelled']).order_by('-order_date')
    context = {
        'orders': orders
    }
    return render(request, 'cheach_history.html', context)




@login_required
def feature(request):
    return render(request, 'feature.html')


# You will need to implement a detailed view for a single order in cheach_history, similar to get_order_details
# For example, order_detail_history(request, order_id)