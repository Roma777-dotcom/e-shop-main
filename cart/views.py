from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shop.models import Product


def get_or_create_cart(request):
    """Получить или создать корзину для текущего пользователя/сессии"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def cart_detail(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


def cart_add(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} добавлен в корзину!")
    return redirect(request.META.get("HTTP_REFERER", "shop:home"))


def cart_remove(request, item_id):
    """Удалить товар из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины!")
    return redirect("cart:cart_detail")


def cart_update(request, item_id):
    """Обновить количество товара в корзине"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get("quantity", 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    messages.success(request, "Корзина обновлена!")
    return redirect("cart:cart_detail")


def cart_clear(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, "Корзина очищена!")
    return redirect("cart:cart_detail")