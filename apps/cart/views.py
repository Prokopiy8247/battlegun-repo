from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from services.cart_service import CartService

@require_GET
def cart_detail(request):
    cart = CartService.get_cart_from_session(request)
    context = {
        'cart_items': cart.items.select_related('product').all(),
        'cart_total': cart.total_price,
        'cart': cart
    }
    return render(request, 'cart/partials/cart_modal.html', context)

@require_POST
def add_to_cart(request, product_id):
    CartService.add_to_cart(request, product_id)
    return cart_detail(request)

@require_POST
def update_cart_item(request, item_id):
    quantity = request.POST.get('quantity')
    CartService.update_quantity(request, item_id, quantity)
    return cart_detail(request)

@require_http_methods(["DELETE", "POST"])
def remove_from_cart(request, item_id):
    CartService.remove_from_cart(request, item_id)
    return cart_detail(request)

@require_GET
def cart_count(request):
    cart = CartService.get_cart_from_session(request)
    # create a small partial via template string or separate file if needed.
    # For now, let's assume we return a simple span or just the number.
    # The user didn't ask for this specifically to be visible yet on frontend, but backend must exist.
    return render(request, 'cart/partials/cart_count.html', {'count': cart.total_items})
