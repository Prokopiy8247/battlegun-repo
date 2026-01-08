from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from .models import Product

def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'products': products,
    }

    if is_htmx(request) and request.headers.get('HX-Target') == 'main-content':
        return render(request, 'catalog/partials/product_list_content.html', context)
    
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }

    if is_htmx(request) and request.headers.get('HX-Target') == 'main-content':
        return render(request, 'catalog/partials/product_detail_content.html', context)

    return render(request, 'catalog/product_detail.html', context)

def home(request):
    # For now, home redirects to catalog or renders catalog as home
    return product_list(request)


# --- Simple Cart Logic (Session Based) ---

def cart_modal(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            item_total = product.price * quantity
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'cart/partials/cart_modal.html', context)

def cart_add(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    
    return cart_modal(request)
