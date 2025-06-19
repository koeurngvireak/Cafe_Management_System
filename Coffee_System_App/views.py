from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomLoginForm
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from decimal import Decimal
# from .models import Drink, Order, OrderItem



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('home')        # Admin
            else:
                return redirect('pos-index')   # Normal user

        else:
            return render(request, 'login/Login.html', {'error': 'Invalid credentials'})

    return render(request, 'login/Login.html')

def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login/logout.html')

def logout_confirm2(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'pos/logout2.html')
    
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
@user_passes_test(lambda u: not u.is_staff)
def pos_system(request):
    return render(request, 'pos/index.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def feature(request):
    return render(request, 'feature.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    return render(request, 'overview.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def orders(request):
    return render(request, 'accept_order.html')
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def inventory(request):
    return render(request, 'pending.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def customers(request):
    return render(request, 'update_drink.html')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def settings(request):
    return render(request, 'cheach_history.html')

@login_required(login_url='login')
@user_passes_test(lambda u: not u.is_staff)
def order_success(request):
    return render(request, 'pos/order_success.html')

def get_cart(request):
    """Retrieves the cart from the session, initializing if it doesn't exist."""
    return request.session.get(settings.CART_SESSION_ID, {})

def save_cart(request, cart):
    """Saves the updated cart back to the session."""
    request.session[settings.CART_SESSION_ID] = cart
    request.session.modified = True
    
@login_required(login_url='login')
@user_passes_test(lambda u: not u.is_staff)
def coffee_menu(request):
    drinks = Drink.objects.all().order_by('name')
    cart = get_cart(request)

    # Populate cart_items with full drink details for rendering
    cart_items = []
    total_cart_price = Decimal('0.00')

    for drink_id_str, item_data in cart.items():
        try:
            drink = Drink.objects.get(id=int(drink_id_str))
            quantity = item_data['quantity']
            price = Decimal(item_data['price']) # Use the price from the cart, not current DB
            item_total = quantity * price
            total_cart_price += item_total
            cart_items.append({
                'id': drink.id,
                'name': drink.name,
                'type': drink.drink_type,
                'price': price,
                'quantity': quantity,
                'total_price': item_total
            })
        except Drink.DoesNotExist:
            # Handle cases where a drink might have been deleted from DB
            del cart[drink_id_str]
            save_cart(request, cart)


    # Sort cart_items by their original order (or name if you prefer)
    # This might require storing an index in the cart or sorting by name
    cart_items_sorted = sorted(cart_items, key=lambda x: x['name']) # Example sort

    context = {
        'drinks': drinks,
        'cart_items': cart_items_sorted,
        'total_cart_price': total_cart_price,
    }
    return render(request, 'pos-index', context)

def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('pos-index') # Redirect if cart is empty

    if request.method == 'POST':
        try:
            order = Order.objects.create(total_amount=Decimal('0.00')) # Will update after adding items
            total_order_amount = Decimal('0.00')

            for drink_id_str, item_data in cart.items():
                drink = Drink.objects.get(id=int(drink_id_str))
                quantity = item_data['quantity']
                price_at_time_of_order = Decimal(item_data['price'])

                OrderItem.objects.create(
                    order=order,
                    drink=drink,
                    quantity=quantity,
                    price=price_at_time_of_order
                )
                total_order_amount += quantity * price_at_time_of_order

            order.total_amount = total_order_amount
            order.is_completed = True # Mark as completed on checkout
            order.save()

            # Clear the cart after successful order
            request.session[settings.CART_SESSION_ID] = {}
            request.session.modified = True

            return redirect('order_success')

        except Exception as e:
            # Log the error and display a user-friendly message
            print(f"Error during checkout: {e}")
            # You might want to add a message to the user here
            return render(request, 'pos/index.html', {'error_message': 'An error occurred during checkout. Please try again.'})

    # For GET request or if something goes wrong before POST
    return redirect('pos-index') # Or render a specific checkout page if you have one







# # Create your views here.
