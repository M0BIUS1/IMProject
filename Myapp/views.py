from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect("studentDashboard")
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "Myapp/login.html")

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
            username = email.split("@")[0]
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
    return render(request, "Myapp/register.html")

def studentDashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "Myapp/studentDashboard.html")

def home_view(request):
    return redirect("login")

def logout_view(request):
    logout(request)
    return redirect("login")
