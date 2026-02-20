from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ-панель для модели User"""
    
    list_display = ["email", "username", "first_name", "last_name", "is_staff", "created_at"]
    list_filter = ["is_staff", "is_superuser", "is_active", "created_at"]
    search_fields = ["email", "username", "first_name", "last_name", "phone"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительная информация", {
            "fields": ("phone", "avatar", "date_of_birth", "address", "city", "postal_code")
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительная информация", {
            "fields": ("email", "phone")
        }),
    )