

from django.shortcuts import render , redirect
from django.contrib.auth.models import User

import random
import http.client
import urllib.parse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')
# def home(request):
#     return render(request,'home.html')
def header(request):
    return render(request,'header.html')

####################new33###############
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile  # Import UserProfile
import pyotp
@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another username.')
            return render(request, 'register1.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use another email.')
            return render(request, 'register1.html')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Ensure the UserProfile is created
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Generate OTP and send email
        otp = user_profile.generate_otp()
        send_otp_via_email(user, otp)

        # Store user ID in session for OTP verification
        request.session['user_id'] = user.id

        messages.success(request, 'User registered successfully! Please check your email for OTP verification.')
        return redirect('Farmer:verify_otp')  # Redirect to OTP verification page
    
    return render(request, 'register1.html')


def send_otp_via_email(user, otp):
    subject = 'Your OTP Code'
    message = f'Welcome to SMARTAGRI Your OTP code is {otp}. It will expire in 5 minutes. \n Leverage the benefits of AI technology of Agriculture'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

def verify_otp_view(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp').strip()  # Trim whitespace

        # Get the user from session
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "No user found for verification.")
            return redirect('Farmer:register')

        user = get_object_or_404(User, id=user_id)
        user_profile = user.userprofile

        # Generate TOTP object with the user's secret
        totp = pyotp.TOTP(user_profile.otp_secret)

        # Verify the entered OTP with a valid time window
        if totp.verify(input_otp, valid_window=1):  # Allows +/- 30 seconds for time drift
            # OTP verification successful
            user_profile.is_verified = True
            user_profile.save()
            request.session.flush()  # Clear session data
            messages.success(request, "OTP verified successfully! You can now login.")
            return redirect('Farmer:login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'otp_input.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'userprofile') and user.userprofile.is_verified:  # Check if the user is verified
                auth_login(request, user)
                return redirect('Farmer:index')  # Redirect to dashboard after login
            else:
                messages.error(request, "Account not verified. Please verify your email OTP.")
                return redirect('verify_otp')  # Redirect to OTP verification if not verified
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'login.html')
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')
