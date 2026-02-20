from django.db import models
from django.conf import settings


class Order(models.Model):
    """Заказ"""
    
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("confirmed", "Подтвержден"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("cancelled", "Отменен"),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Номер заказа")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name="orders",
        null=True, 
        verbose_name="Пользователь"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="pending", 
        verbose_name="Статус"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    
    # Данные доставки
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес доставки")
    city = models.CharField(max_length=100, verbose_name="Город")
    postal_code = models.CharField(max_length=20, verbose_name="Почтовый индекс")
    delivery_notes = models.TextField(blank=True, verbose_name="Примечания к доставке")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Заказ {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Генерация уникального номера заказа"""
        import uuid
        return str(uuid.uuid4()).split("-")[0].upper()
    
    def get_total_items(self):
        """Общее количество товаров в заказе"""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Элемент заказа"""
    
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, 
        related_name="items", verbose_name="Заказ"
    )
    product = models.ForeignKey(
        "shop.Product", on_delete=models.SET_NULL, 
        null=True, verbose_name="Товар"
    )
    product_name = models.CharField(max_length=200, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"
        ordering = ["id"]
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def get_total_price(self):
        """Стоимость товара с учетом количества"""
        return self.price * self.quantity


class Payment(models.Model):
    """Оплата заказа"""
    
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличными при получении"),
        ("card", "Картой при получении"),
        ("online", "Онлайн оплата"),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка оплаты"),
        ("refunded", "Возвращено"),
    ]
    
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, 
        related_name="payment", verbose_name="Заказ"
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        verbose_name="Способ оплаты"
    )
    status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default="pending", 
        verbose_name="Статус оплаты"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    transaction_id = models.CharField(max_length=255, blank=True, verbose_name="ID транзакции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Оплата заказа {self.order.order_number}"