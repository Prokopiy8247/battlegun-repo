from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderForm
from services.cart_service import CartService

def checkout(request):
    cart = CartService.get_cart_from_session(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.subtotal = cart.total_price  # Assuming cart matches order logic
                    order.total = order.subtotal + order.shipping_cost
                    order.save()

                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            product_sku=item.product.sku,
                            price=item.price,
                            quantity=item.quantity,
                            subtotal=item.total_price
                        )
                    
                    # Do NOT clear cart yet if we want persistence until payment? 
                    # Usually e-comm clears cart after order placement.
                    # Use cart_service to clear.
                    CartService.clear_cart(request)
                    
                    return redirect('payment_start', order_id=order.id)
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart,
        'cart_total': cart.total_price
    }
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/confirmation.html', {'order': order})
