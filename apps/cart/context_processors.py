from services.cart_service import CartService

def cart(request):
    cart = CartService.get_cart_from_session(request)
    return {
        'cart': cart
    }
