from django.db import models
from django.conf import settings

class Cart(models.Model):
    """Корзина покупок"""
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="cart",
        null=True, 
        blank=True,
        verbose_name="Пользователь"
    )
    session_key = models.CharField(max_length=255, blank=True, verbose_name="Ключ сессии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Корзина {self.id}"
    
    def get_total_price(self):
        """Общая стоимость товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, 
        related_name="items", verbose_name="Корзина"
    )
    product = models.ForeignKey(
        "shop.Product", on_delete=models.CASCADE, 
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        ordering = ["-created_at"]
        unique_together = ["cart", "product"]
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total_price(self):
        """Стоимость товара с учетом количества"""
        return self.product.price * self.quantity