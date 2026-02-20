from .models import Cart, CartItem


def cart_context(request):
    """Контекст-процессор для добавления корзины в контекст всех шаблонов"""
    cart = None
    cart_items_count = 0
    cart_total_price = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    if cart:
        cart_items_count = cart.get_total_items()
        cart_total_price = cart.get_total_price()
    
    return {
        "cart": cart,
        "cart_items_count": cart_items_count,
        "cart_total_price": cart_total_price,
    }
