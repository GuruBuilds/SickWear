from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.models import Address

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
        # Extracting user information from the form
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        phone = request.POST['phone']

        # Extracting address information from the form
        street_address = request.POST['street_address']
        apartment_number = request.POST.get('apartment_number', '')
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pincode = request.POST['pincode']
        is_default = 'is_default' in request.POST  # Checking if the address is marked as default

        # Validation checks
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        # Creating the user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.name = name
        new_user.phone_number = phone
        new_user.save()

        # Create an Address instance for the user
        new_address = Address(
            user=new_user,
            street_address=street_address,
            apartment_number=apartment_number,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            is_default=is_default
        )
        new_address.save()

        messages.success(request, 'You have successfully signed up.')

        # Log the user in and redirect to the home page
        user_login = authenticate(username=username, password=password)
        login(request, user_login)
        return redirect('/')

    return render(request, 'authentication/signup.html')

def signout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')
