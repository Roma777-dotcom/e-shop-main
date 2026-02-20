from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    """Инлайн для элементов корзины"""
    model = CartItem
    extra = 0
    readonly_fields = ["product", "quantity", "get_total_price"]
    fields = ["product", "quantity", "get_total_price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ-панель для корзины"""
    list_display = ["id", "user", "session_key", "get_total_items", "get_total_price", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "session_key"]
    readonly_fields = ["get_total_price", "get_total_items"]
    ordering = ["-created_at"]
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Админ-панель для элементов корзины"""
    list_display = ["cart", "product", "quantity", "get_total_price", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["product__name"]
    readonly_fields = ["get_total_price"]
    ordering = ["-created_at"]