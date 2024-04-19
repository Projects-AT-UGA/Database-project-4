from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Clerk,MenuItem,Cart, Contains


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages


def home(request):
    is_authenticated = request.user.is_authenticated
    is_clerk = hasattr(request.user, 'clerk')

    # Check if login failed due to wrong password
    if request.method == 'POST' and not is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            error_message = "Invalid username or password."
            return render(request, 'home.html', {'error_message': error_message})

    # Check if user is not a clerk
    if not is_clerk:
        error_message = "You need to be a clerk to access this page."
        return render(request, 'home.html', {'error_message': error_message})

    menu_items = MenuItem.objects.all()  # Retrieve all menu items

    return render(request, 'home.html', {'is_authenticated': is_authenticated, 'menu_items': menu_items})






@login_required
def update_cart(request):
    if request.method == 'POST':
        # Retrieve customer information from the form
        customer_user_name = request.POST.get('customer_user_name')
        customer_mobile_number = request.POST.get('customer_mobile_number')

        # Update customer information in the associated cart object
        clerk = request.user.clerk
        cart = Cart.objects.filter(clerk=clerk).first()
        if cart:
            cart.customer_user_name = customer_user_name
            cart.customer_mobile_number = customer_mobile_number
            cart.save()

        # Loop through all POST data to update quantities of items in the cart
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = key.split('_')[1]
                cart_item = get_object_or_404(Contains, pk=item_id)
                cart_item.quantity = value
                cart_item.save()

    # Redirect back to the cart page after updating the quantities and customer information
    return redirect('cart')




@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, pk=menu_item_id)
    clerk = request.user.clerk

    # Check if a cart exists for the clerk, otherwise create a new cart
    cart, created = Cart.objects.get_or_create(clerk=clerk)

    # Check if the menu item already exists in the cart
    existing_item = cart.contains_set.filter(menu_item=menu_item).first()

    if existing_item:
        # If the item exists, increase its quantity
        existing_item.quantity += 1
        existing_item.save()
        messages.success(request, f"{menu_item.menu_item_name} quantity increased in cart.")
    else:
        # If the item does not exist, add it to the cart with quantity 1
        new_item = Contains.objects.create(cart=cart, menu_item=menu_item, quantity=1)
        messages.success(request, f"{menu_item.menu_item_name} added to cart.")

    return redirect('home')

@login_required
def cart(request):
    clerk = request.user.clerk
    cart_items = Cart.objects.filter(clerk=clerk).first()
    return render(request, 'cart.html', {'cart_items': cart_items})






def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        error_message = "Invalid username or password."
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        if username and password and email and mobile_number:
            user = User.objects.create_user(username=username, email=email, password=password)
            clerk = Clerk.objects.create(user=user, email=email, mobile_number=mobile_number)
            clerk.save()
            return redirect('login')
        error_message = "All fields are required for signup."
        return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')
