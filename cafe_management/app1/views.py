from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Clerk, MenuItem,Cart,Order,OrderItem
# from .models import MenuItem,Cart, Contains, Order, OrderedItem,Payment

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
import json


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






# @login_required
# def update_cart(request):
#     if request.method == 'POST':
#         # Retrieve customer information from the form
#         customer_user_name = request.POST.get('customer_user_name')
#         customer_mobile_number = request.POST.get('customer_mobile_number')

#         # Update customer information in the associated cart object
#         clerk = request.user.clerk
#         cart = Cart.objects.filter(clerk=clerk).first()
#         if cart:
#             cart.customer_user_name = customer_user_name
#             cart.customer_mobile_number = customer_mobile_number
#             cart.save()

#         # Loop through all POST data to update quantities of items in the cart
#         for key, value in request.POST.items():
#             if key.startswith('quantity_'):
#                 item_id = key.split('_')[1]
#                 cart_item = get_object_or_404(Contains, pk=item_id)
#                 cart_item.quantity = value
#                 cart_item.save()

#     # Redirect back to the cart page after updating the quantities and customer information
#     return redirect('cart')


@login_required

def add_to_cart(request, menu_item_id):
    # Retrieve the menu item object
    menu_item = MenuItem.objects.get(pk=menu_item_id)

    # Retrieve the logged-in user (clerk)
    clerk = Clerk.objects.get(user=request.user)

    # Check if there is an existing cart for the clerk
    try:
        cart = Cart.objects.get(clerk=clerk)
    except Cart.DoesNotExist:
        # If cart doesn't exist, create a new order with status 0 (Pending)
        order = Order.objects.create(clerk=clerk, status=0)
        # Create a new cart with the order_id
        cart = Cart.objects.create(order_id=order.pk, clerk=clerk)

    # If the cart already exists, get the order_id from it
    order_id = cart.order_id 
    print(order_id)
    print(clerk.user.username)
    order = Order.objects.get(pk=order_id)
    if(order.status):
         order = Order.objects.create(clerk=clerk, status=0)
         cart.order_id = order.id
         cart.save()
    #If order_menu_item exists
    order_id = cart.order_id

    # Check if an OrderItem already exists for the given order_id and menu_item_id
    order_item = OrderItem.objects.filter(order_id=order_id, menu_item=menu_item)

    if not order_item.exists():
        # If the OrderItem doesn't exist, create a new one
        OrderItem.objects.create(order_id=order_id, menu_item=menu_item)
    else:
        # If the OrderItem already exists, you can handle it as needed
        
        order_item = OrderItem.objects.get(order_id=order_id, menu_item=menu_item)
        order_item.quantity += 1 
        order_item.save()

    print(order_item)


    return redirect('home')

def checkout(request):
    
    clerk = Clerk.objects.get(user=request.user)
    try:
        cart = Cart.objects.get(clerk=clerk)
    except Cart.DoesNotExist:
        render(request, 'home.html')
    total_payment,order_items = calculate_total_payment(cart)
    
    print(total_payment)
    print(order_items)
    print(cart.order_id)
    order = Order.objects.get(pk=cart.order_id)
    # order.status = 1
    # order.save()
    print("Order")
    print(order)
    print(order_items)
    print("Render")
    return render(request, 'order_confirmation.html', {'order': order, 'ordered_items': order_items,'total_payment': total_payment},)

def calculate_total_payment(cart):
    total_payment = 0
    ordered_items =  OrderItem.objects.filter(order_id=cart.order_id)
    # Iterate through each order item in the cart
    for order_item in  ordered_items:
        # Add the price of each menu item multiplied by its quantity to the total payment
        total_payment += order_item.menu_item.price * order_item.quantity
    
    return total_payment,ordered_items

@login_required
def view_cart(request):
    clerk = Clerk.objects.get(user=request.user)
    try:
        cart = Cart.objects.get(clerk=clerk)
    except Cart.DoesNotExist:
        render(request, 'home.html')

    order = Order.objects.get(pk=cart.order_id)
    if order.status:
        render(request, 'home.html')


    cart_items = OrderItem.objects.filter(order_id=cart.order_id)

    return render(request, 'view_cart.html', {'cart_items': cart_items})



def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    ordered_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'ordered_items': ordered_items})



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



def update_quantity(request):
    if request.method == 'POST':
        print("+_+_+_")
        print(request)
        #item_id = request.POST.get('item_id')
        #item_id =1
        #action = request.POST.get('action')
        #print(request.POST.get_query_set())

        payload = json.loads(request.body)  # Load JSON data from the body
        item_id = payload.get("item_id")
        action = payload.get("action")

        # Retrieve the cart item from the database
        # order = Order.objects.get(pk=cart.order_id)
        print(item_id)
        if not item_id:
            return JsonResponse({'error': 'Invalid request method'})
        order_item = OrderItem.objects.get(pk=item_id)

        print(order_item)
        # Update the quantity based on the action
        if action == 'decrement':
            order_item.quantity -= 1
        elif action == 'increment':
            order_item.quantity += 1

        # Save the changes to the database
        order_item.save()
        print("HERE")
        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    # If the request method is not POST, return a JSON response with an error
    return JsonResponse({'error': 'Invalid request method'})
# # views.py




# def calculate_total_payment(cart):
#     total_payment = 0
#     if cart:
#         for contains_item in cart.contains_set.all():
#             total_payment += contains_item.menu_item.price * contains_item.quantity
#     return total_payment

# def create_order(cart, total_payment, payment_type):
#     if cart:
#         clerk = cart.clerk
#         customer_user_name = cart.customer_user_name
#         customer_mobile_number = cart.customer_mobile_number
        
#         order = Order.objects.create(clerk=clerk,  
#                                      customer_user_name=customer_user_name, customer_mobile_number=customer_mobile_number)
#         for contains_item in cart.contains_set.all():
#             OrderedItem.objects.create(order=order, ordered_item_name=contains_item.menu_item.menu_item_name, 
#                                         category=contains_item.menu_item.category, price=contains_item.menu_item.price, 
#                                         quantity=contains_item.quantity)
#         payment=Payment.objects.create(order=order,total_payment=total_payment, payment_type=payment_type)
#         order.payment_id=payment.id
#         order.save()
#         return order
#     return None

# def clear_cart(cart):
#     if cart:
#         cart.contains_set.all().delete()
# def order_confirmation(request, order_id):
#     order = get_object_or_404(Order, pk=order_id)
#     ordered_items = OrderedItem.objects.filter(order=order)
#     return render(request, 'order_confirmation.html', {'order': order, 'ordered_items': ordered_items})





