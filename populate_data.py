import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from shop.models import Category, Product, ProductImage

# Создаем категории
categories_data = [
    {
        "name": "Смартфоны",
        "slug": "smartfony",
        "description": "Современные смартфоны от ведущих производителей",
    },
    {
        "name": "Ноутбуки",
        "slug": "noutbuki",
        "description": "Мощные и стильные ноутбуки для работы и развлечений",
    },
    {
        "name": "Планшеты",
        "slug": "planshety",
        "description": "Планшеты для работы, учебы и развлечений",
    },
    {
        "name": "Аксессуары",
        "slug": "aksessuary",
        "description": "Чехлы, зарядки и другие аксессуары для гаджетов",
    },
    {
        "name": "Аудиотехника",
        "slug": "audiotekhnika",
        "description": "Наушники, колонки и другая аудиотехника",
    },
]

print("Создание категорий...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data["slug"],
        defaults={
            "name": cat_data["name"],
            "description": cat_data["description"],
        }
    )
    if created:
        print(f"  Категория '{category.name}' создана")
    else:
        print(f"  Категория '{category.name}' уже существует")

# Создаем товары
products_data = [
    {
        "name": "iPhone 15 Pro Max",
        "slug": "iphone-15-pro-max",
        "description": "Флагманский смартфон Apple с процессором A17 Pro, 256GB памяти, титановый корпус",
        "price": 149990,
        "old_price": 159990,
        "stock": 10,
        "category_slug": "smartfony",
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "slug": "samsung-galaxy-s24-ultra",
        "description": "Флагманский смартфон Samsung с S Pen, 512GB памяти, камера 200 МП",
        "price": 129990,
        "stock": 8,
        "category_slug": "smartfony",
    },
    {
        "name": "Xiaomi 14 Ultra",
        "slug": "xiaomi-14-ultra",
        "description": "Флагманский смартфон Xiaomi с камерой Leica, 512GB памяти",
        "price": 99990,
        "old_price": 109990,
        "stock": 12,
        "category_slug": "smartfony",
    },
    {
        "name": "MacBook Pro 14\"",
        "slug": "macbook-pro-14",
        "description": "Ноутбук Apple с чипом M3 Pro, 18GB RAM, 512GB SSD",
        "price": 199990,
        "old_price": 219990,
        "stock": 5,
        "category_slug": "noutbuki",
    },
    {
        "name": "ASUS ROG Zephyrus G14",
        "slug": "asus-rog-zephyrus-g14",
        "description": "Игровой ноутбук с процессором AMD Ryzen 9, RTX 4060, 16GB RAM",
        "price": 149990,
        "stock": 7,
        "category_slug": "noutbuki",
    },
    {
        "name": "iPad Pro 12.9\"",
        "slug": "ipad-pro-12-9",
        "description": "Планшет Apple с чипом M2, 256GB памяти, дисплей Liquid Retina XDR",
        "price": 119990,
        "stock": 6,
        "category_slug": "planshety",
    },
    {
        "name": "Samsung Galaxy Tab S9+",
        "slug": "samsung-galaxy-tab-s9-plus",
        "description": "Планшет Samsung с AMOLED дисплеем, S Pen, 256GB памяти",
        "price": 89990,
        "stock": 9,
        "category_slug": "planshety",
    },
    {
        "name": "AirPods Pro 2",
        "slug": "airpods-pro-2",
        "description": "Беспроводные наушники Apple с активным шумоподавлением",
        "price": 24990,
        "old_price": 27990,
        "stock": 20,
        "category_slug": "audiotekhnika",
    },
    {
        "name": "Sony WH-1000XM5",
        "slug": "sony-wh-1000xm5",
        "description": "Полноразмерные наушники с лучшим в классе шумоподавлением",
        "price": 34990,
        "stock": 15,
        "category_slug": "audiotekhnika",
    },
    {
        "name": "JBL Charge 5",
        "slug": "jbl-charge-5",
        "description": "Портативная колонка с мощным звуком и защитой от воды",
        "price": 12990,
        "stock": 25,
        "category_slug": "audiotekhnika",
    },
    {
        "name": "Чехол для iPhone 15 Pro",
        "slug": "chehol-iphone-15-pro",
        "description": "Защитный чехол из премиального материала для iPhone 15 Pro",
        "price": 2990,
        "stock": 50,
        "category_slug": "aksessuary",
    },
    {
        "name": "Зарядное устройство 65W",
        "slug": "zaryadnoe-65w",
        "description": "Быстрая зарядка 65W с поддержкой Power Delivery",
        "price": 3990,
        "stock": 30,
        "category_slug": "aksessuary",
    },
]

print("\nСоздание товаров...")
for prod_data in products_data:
    category = Category.objects.get(slug=prod_data["category_slug"])
    
    product, created = Product.objects.get_or_create(
        slug=prod_data["slug"],
        defaults={
            "name": prod_data["name"],
            "description": prod_data["description"],
            "price": prod_data["price"],
            "old_price": prod_data.get("old_price"),
            "stock": prod_data["stock"],
            "available": prod_data["stock"] > 0,
            "category": category,
        }
    )
    
    if created:
        print(f"  Товар '{product.name}' создан")
    else:
        print(f"  Товар '{product.name}' уже существует")

print("\nЗаполнение базы данных завершено!")
print(f"Всего категорий: {Category.objects.count()}")
print(f"Всего товаров: {Product.objects.count()}")
