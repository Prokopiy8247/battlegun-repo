from django.shortcuts import render
from services.cart_service import CartService

def get_cart_context(request):
    """Helper to get consistent cart context."""
    cart = CartService.get_cart_from_session(request)
    return {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all().order_by('product__name'),
        'cart_total': cart.total_price,
    }

def cart_detail(request):
    context = get_cart_context(request)
    return render(request, 'cart/partials/cart_modal.html', context)

def add_to_cart(request, product_id):
    CartService.add_to_cart(request, product_id)
    return cart_detail(request)

def update_cart_item(request, item_id):
    quantity = request.POST.get('quantity')
    if quantity is not None:
        CartService.update_quantity(request, item_id, quantity)
    return cart_detail(request)

def remove_from_cart(request, item_id):
    CartService.remove_from_cart(request, item_id)
    return cart_detail(request)

def cart_count(request):
    cart = CartService.get_cart_from_session(request)
    return render(request, 'cart/partials/cart_count.html', {'count': cart.total_items})
