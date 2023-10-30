from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user
from django.db.models import Q

def index(request):
    categories = Categories.objects.all()
    selected_category = request.GET.get('category')
    query = request.GET.get('q')
    sort_option = request.GET.get('sort')  # Get the sort option from the URL

    items = Item.objects.all()

    if selected_category:
        items = items.filter(category__name=selected_category)

    if query:
        items = items.filter(Q(name__icontains=query))

    if sort_option == 'low_to_high':
        items = items.order_by('price')
    elif sort_option == 'high_to_low':
        items = items.order_by('-price')

    context = {
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
        'query': query
    }

    return render(request, "index.html", context)


@login_required
def AddToCartView(request, item_id):
    item = Item.objects.get(item_id=item_id)
    user = request.user
    # Check if there is an existing cart item with the same item and 'in_cart' status
    existing_cart_item = CartItem.objects.filter(user=user, item=item, status='in_cart').first()

    if existing_cart_item:
        # If an item with 'in_cart' status already exists, increment its quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
        message = 'Item added to the cart successfully.'
    else:
        # If there is no item with 'in_cart' status, create a new cart item
        new_cart_item = CartItem(user=user, item=item, quantity=1, status='in_cart')
        new_cart_item.save()
        message = 'Item added to the cart successfully.'

    return JsonResponse({'message': message})

@login_required
def CartView(request):
    cart_items = CartItem.objects.filter(user=request.user, status='in_cart')
    total_bill = calculate_total_bill(cart_items)
    context = {'cart_items': cart_items, 'total_bill': total_bill}
    return render(request, 'cart.html', context)

@login_required
def RemoveFromCartView(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        message = 'Item removed from the cart.'
    except CartItem.DoesNotExist:
        message = 'Item not found in the cart'

    return JsonResponse({'message': message})


def calculate_total_bill(cart_items):
    total = sum(float(item.item.price) * item.quantity for item in cart_items)
    return total

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login sucess")
            return redirect('index')  # Replace 'index' with your desired redirect URL
        else:
            messages.error(request, 'Invalid Login Credentials')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')  # Replace 'index' with your desired redirect URL
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'login.html')


@login_required

def logout_view(request):
    logout(request)
    return redirect('index') 

@login_required
def process_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        location = request.POST.get('location')

        # Get the current user and cart items with 'in_cart' status
        user = request.user
        cart_items = CartItem.objects.filter(user=user, status='in_cart')

        # Calculate the total price
        total_price = calculate_total_bill(cart_items)

        # Create a new order
        order = Order(user=user, total_price=total_price, name=name, phone=mobile, location=location)
        order.save()
        order.items.set(cart_items)  # Add cart items to the order

        # Update the status of cart items to 'ordered'
        cart_items.update(status='ordered')

        return redirect('index')  # Redirect to the index page or a thank you page

    # If it's a GET request, you can pass the cart items and other details to the checkout.html template
    elif request.method == 'GET':
            if not request.user.is_authenticated:
                return redirect('login')

            # Get the current user and their cart items with 'pending' status
            user = request.user
            cart_items = CartItem.objects.filter(user=user, status='in_cart')

            # Calculate the total price
            total_price = calculate_total_bill(cart_items)

            context = {
                'cart_items': cart_items,
                'total_bill': total_price,
            }

            return render(request, 'checkout.html', context)
        
@login_required
def order_view(request):
    # Get orders for the currently logged-in user
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }

    return render(request, 'order.html', context)



