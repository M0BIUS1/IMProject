from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re

# -----------------------
# Login page
# -----------------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # authenticate using email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "Myapp/login.html")

# -----------------------
# Register page
# -----------------------
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        errors = {}

        # Required fields
        if not name:
            errors['name'] = "Full Name is required"
        if not email:
            errors['email'] = "Email is required"
        if not password:
            errors['password'] = "Password is required"
        if not confirm_password:
            errors['confirm_password'] = "Confirm Password is required"

        # Email format check
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if email and not re.match(email_pattern, email):
            errors['email'] = "Please enter a valid email address"

        # Password strength
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if password and not re.match(password_pattern, password):
            errors['password'] = "Password must be 8+ chars, include uppercase, number & symbol"

        # Password confirmation
        if password and confirm_password and password != confirm_password:
            errors['confirm_password'] = "Passwords do not match"

        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            errors['email'] = "Email is already registered"

        if errors:
            # Send errors to template
            return render(request, "Myapp/register.html", {
                'errors': errors,
                'name': name,
                'email': email,
            })

        # Generate a username from email
        username = email.split("@")[0]

        # Create user in database
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "Myapp/register.html")

# -----------------------
# Home redirect
# -----------------------
def home_view(request):
    return redirect('login')

# -----------------------
# Logout
# -----------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

# -----------------------
# Dashboard
# -----------------------
def student_dashboard_view(request):
    return render(request, "Myapp/studentDashboard.html")
