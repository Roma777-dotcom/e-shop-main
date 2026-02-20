from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Категория товаров"""
    
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    """Товар"""
    
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True, verbose_name="Старая цена"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        related_name="products", verbose_name="Категория"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created_at"]),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})
    
    def is_in_stock(self):
        return self.stock > 0
    
    def get_discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    """Изображения товара"""
    
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name="images", verbose_name="Товар"
    )
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Альтернативный текст")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ["-is_main", "created_at"]
    
    def __str__(self):
        return f"{self.product.name} - {self.id}"