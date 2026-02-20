from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegisterForm, UserEditForm
from .models import User


def register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались! Теперь вы можете войти.")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    """Выход из системы (поддерживает GET и POST)"""
    logout(request)
    messages.success(request, "Вы успешно вышли из системы!")
    return redirect("shop:home")


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    orders = request.user.orders.all()[:5]
    return render(request, "accounts/profile.html", {"orders": orders})


@login_required
def profile_edit(request):
    """Редактирование профиля"""
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("accounts:profile")
    else:
        form = UserEditForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})