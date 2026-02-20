from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem, Payment
from .forms import OrderCreateForm
from cart.models import Cart, CartItem
from shop.models import Product


@login_required
@transaction.atomic
def order_create(request):
    """Оформление заказа"""
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста!")
        return redirect("shop:home")
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                total_price=cart.get_total_price(),
                **{k: v for k, v in form.cleaned_data.items() if k != "payment_method"}
            )
            
            # Создаем элементы заказа
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    product_name=cart_item.product.name,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                
                # Обновляем количество товара
                product = cart_item.product
                product.stock = max(0, product.stock - cart_item.quantity)
                if product.stock == 0:
                    product.available = False
                product.save()
            
            # Создаем оплату
            Payment.objects.create(
                order=order,
                payment_method=form.cleaned_data["payment_method"],
                amount=cart.get_total_price(),
                status="paid" if form.cleaned_data["payment_method"] == "online" else "pending"
            )
            
            # Обновляем статус заказа
            if form.cleaned_data["payment_method"] == "online":
                order.status = "confirmed"
            order.save()
            
            # Очищаем корзину
            cart.items.all().delete()
            
            messages.success(request, "Заказ успешно оформлен!")
            return redirect("orders:order_success", order_number=order.order_number)
    else:
        # Предзаполняем форму данными пользователя
        initial_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "phone": request.user.phone or "",
            "address": request.user.address or "",
            "city": request.user.city or "",
            "postal_code": request.user.postal_code or "",
        }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, "orders/order_create.html", {"form": form, "cart": cart})


@login_required
def order_success(request, order_number):
    """Страница успешного заказа"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})


@login_required
def order_history(request):
    """История заказов"""
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_number):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})