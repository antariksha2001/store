from decimal import Decimal


def cart(request):
    """Context processor to make cart available in all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(int(item['quantity']) for item in cart.values())
    cart_total = sum(Decimal(item['price']) * int(item['quantity']) for item in cart.values())
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }
