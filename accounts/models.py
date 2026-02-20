from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя"""
    
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    address = models.TextField(blank=True, verbose_name="Адрес доставки")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Почтовый индекс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.email or self.username