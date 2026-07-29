from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account created successfully")
            return redirect("login")

    return render(request, "signup.html")

@login_required
def profile_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Email already exists")
        else:
            user = request.user
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully")
        return redirect("profile")
    return render(request, "profile.html")  

@login_required
def change_password_view(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect")

        elif new_password != confirm_new_password:
            messages.error(request, "New passwords do not match")

        else:
            request.user.set_password(new_password)
            request.user.save()

            messages.success(request, "Password changed successfully")
            return redirect("login")

    return render(request, "change_password.html")