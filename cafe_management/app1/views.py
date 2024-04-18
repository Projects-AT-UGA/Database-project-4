from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Clerk,MenuItem


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
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
