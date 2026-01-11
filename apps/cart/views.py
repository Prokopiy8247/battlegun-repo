from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from services.cart_service import CartService

def cart_detail(request):
    cart = CartService.get_cart_from_session(request)
    context = {
        'cart_items': cart.items.select_related('product').all(),
        'cart_total': cart.total_price,
        'cart': cart
    }
    return render(request, 'cart/partials/cart_modal.html', context)

@csrf_exempt
def add_to_cart(request, product_id):
    print(f"DEBUG: add_to_cart called with {product_id}, method={request.method}")
    CartService.add_to_cart(request, product_id)
    return cart_detail(request)

@csrf_exempt
def update_cart_item(request, item_id):
    print(f"DEBUG: update_cart_item called with {item_id}, method={request.method}")
    quantity = request.POST.get('quantity')
    CartService.update_quantity(request, item_id, quantity)
    return cart_detail(request)

@csrf_exempt
def remove_from_cart(request, item_id):
    print(f"DEBUG: remove_from_cart called with {item_id}, method={request.method}")
    CartService.remove_from_cart(request, item_id)
    return cart_detail(request)

def cart_count(request):
    cart = CartService.get_cart_from_session(request)
    return render(request, 'cart/partials/cart_count.html', {'count': cart.total_items})
