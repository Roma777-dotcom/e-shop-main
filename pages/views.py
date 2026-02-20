from django.shortcuts import render

# Create your views here.

def about(request):
    """Страница О нас"""
    return render(request, "pages/about.html")

def delivery(request):
    """Страница Доставка"""
    return render(request, "pages/delivery.html")

def payment(request):
    """Страница Оплата"""
    return render(request, "pages/payment.html")

def contacts(request):
    """Страница Контакты"""
    return render(request, "pages/contacts.html")