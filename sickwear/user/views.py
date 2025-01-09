from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

User = get_user_model()
# Create your views here.

def signin(request):
    if request.method == 'POST':
        login_input = request.POST['email']  # Can be email or username
        password = request.POST['password']
        # Check if login input is an email
        try:
            user = User.objects.get(email=login_input)
            username = user.username
        except User.DoesNotExist:
            username = login_input  # Assume it's a username if not an email
        # Authenticate with the resolved username
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('signin')
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        phone = request.POST['phone']
        address = request.POST['address']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.name = name
        new_user.phone_number = phone
        new_user.address = address
        new_user.save()
        messages.success(request, 'You have successfully signed up.')
        #log user in and redirect to settings page
        user_login = authenticate(username=username, password=password)
        login(request, user_login)
        return redirect('/')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')
