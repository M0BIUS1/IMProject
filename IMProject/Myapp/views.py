from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            # generate a username from email
            username = email.split("@")[0]

            # create user in database
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
