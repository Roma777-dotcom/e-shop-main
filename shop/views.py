from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min, Max
from .models import Product, Category
from .forms import ProductFilterForm


def home(request):
    """Главная страница - каталог товаров"""
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    current_category = None
    
    # Фильтрация
    category_slug = request.GET.get("category")
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    
    # Поиск
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Фильтр по цене
    filter_form = ProductFilterForm(request.GET)
    if filter_form.is_valid():
        min_price = filter_form.cleaned_data.get("min_price")
        max_price = filter_form.cleaned_data.get("max_price")
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
    
    # Сортировка
    sort = request.GET.get("sort")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "name_asc":
        products = products.order_by("name")
    elif sort == "name_desc":
        products = products.order_by("-name")
    elif sort == "newest":
        products = products.order_by("-created_at")
    
    # Получаем минимальную и максимальную цену
    price_range = Product.objects.aggregate(
        min_price=Min("price"), 
        max_price=Max("price")
    )
    
    context = {
        "products": products,
        "categories": categories,
        "current_category": current_category,
        "filter_form": filter_form,
        "price_range": price_range,
    }
    return render(request, "shop/home.html", context)


def category_detail(request, slug):
    """Детальная страница категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "shop/category_detail.html", context)


def product_detail(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "shop/product_detail.html", context)


def search(request):
    """Поиск товаров"""
    query = request.GET.get("q")
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            available=True
        )
    
    context = {
        "products": products,
        "query": query,
    }
    return render(request, "shop/search.html", context)