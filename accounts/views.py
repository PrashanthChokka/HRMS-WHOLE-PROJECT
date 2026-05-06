from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Registration
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# ---------- REGISTER ----------

def register(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")

        # -------- VALIDATIONS --------

        # ✅ Strong password validation (uses AUTH_PASSWORD_VALIDATORS)
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect("register")

        # ✅ Mobile validation
        if not mobile.isdigit() or len(mobile) != 10:
            messages.error(request, "Mobile must be 10 digits")
            return redirect("register")

        # ✅ Check existing user
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        # -------- CREATE DJANGO USER (PASSWORD HASHED AUTOMATICALLY) --------

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,  # ✅ Django hashes internally
            first_name=first_name,
            last_name=last_name
        )

        # -------- CREATE REGISTRATION PROFILE (NO PASSWORD STORED) --------

        Registration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            gender=gender
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "accounts/register.html")


# ---------- LOGIN ----------

def login_view(request):

    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("base")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html")


# ---------- LOGOUT ----------

def logout_view(request):
    logout(request)
    return redirect("login")


# ---------- DASHBOARD ----------

@login_required
def base_view(request):
    return render(request, "employee/base.html")