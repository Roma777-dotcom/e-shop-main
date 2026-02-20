from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    """Инлайн для элементов заказа"""
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name", "price", "quantity", "get_total_price"]
    fields = ["product", "product_name", "price", "quantity", "get_total_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админ-панель для заказов"""
    list_display = [
        "order_number", "user", "status", "total_price", 
        "first_name", "last_name", "created_at"
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["order_number", "user__email", "first_name", "last_name", "email"]
    readonly_fields = [
        "order_number", "get_total_items", "created_at", "updated_at"
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    
    fieldsets = (
        ("Информация о заказе", {
            "fields": ("order_number", "user", "status", "total_price", "get_total_items")
        }),
        ("Информация о покупателе", {
            "fields": ("first_name", "last_name", "email", "phone")
        }),
        ("Адрес доставки", {
            "fields": ("address", "city", "postal_code", "delivery_notes")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Админ-панель для элементов заказа"""
    list_display = ["order", "product_name", "price", "quantity", "get_total_price"]
    list_filter = ["order__status"]
    search_fields = ["order__order_number", "product_name"]
    readonly_fields = ["get_total_price"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Админ-панель для оплат"""
    list_display = ["order", "payment_method", "status", "amount", "created_at"]
    list_filter = ["payment_method", "status", "created_at"]
    search_fields = ["order__order_number", "transaction_id"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]