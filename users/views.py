from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from courses.models import Enrollment, Course, Review

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome {user.username}! Your account has been created."
            )
            return redirect("dashboard")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/signup.html", {"form": form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")


@require_http_methods(["POST"])
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def user_profile(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("user_profile")
    else:
        form = CustomUserChangeForm(instance=user)

    context = {
        "form": form,
        "user": user,
    }
    return render(request, "users/profile.html", context)


@login_required
def dashboard(request):
    user = request.user

    if user.is_student():
        enrolled_courses = Enrollment.objects.filter(student=user).select_related(
            "course"
        )
        context = {
            "enrolled_courses": enrolled_courses,
            "is_student": True,
        }
        return render(request, "users/student_dashboard.html", context)

    elif user.is_instructor():
        courses = user.courses.all()
        context = {
            "courses": courses,
            "is_instructor": True,
        }
        return render(request, "users/instructor_dashboard.html", context)

    elif user.is_admin():
        courses_count = Course.objects.count()
        users_count = User.objects.count()
        enrollments_count = Enrollment.objects.count()
        reviews_count = Review.objects.count()
        context = {
            "is_admin": True,
            "courses_count": courses_count,
            "users_count": users_count,
            "enrollments_count": enrollments_count,
            "reviews_count": reviews_count,
        }
        return render(request, "users/admin_dashboard.html", context)

    return redirect("home")
