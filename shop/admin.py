from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Инлайн для изображений товара"""
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_main"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категории"""
    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для товара"""
    list_display = ["name", "category", "price", "old_price", "stock", "available", "created_at"]
    list_filter = ["category", "available", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["-created_at"]
    inlines = [ProductImageInline]
    date_hierarchy = "created_at"
    
    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "slug", "description", "category")
        }),
        ("Цена и наличие", {
            "fields": ("price", "old_price", "stock", "available")
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Админ-панель для изображений товара"""
    list_display = ["product", "alt_text", "is_main", "created_at"]
    list_filter = ["is_main", "created_at"]
    search_fields = ["product__name", "alt_text"]