from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

User = get_user_model()
# Create your views here.

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
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
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        phone = request.POST['phone']
        address = request.POST['address']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')
        new_user = User.objects.create_user(username=email, email=email, password=password)
        new_user.phone_number = phone
        new_user.address = address
        new_user.save()
        messages.success(request, 'You have successfully signed up.')
        #log user in and redirect to settings page
        user_login = authenticate(username=email, password=password)
        login(request, user_login)
        return redirect('/')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')
