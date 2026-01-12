from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse
from .models import Order, OrderItem
from .forms import OrderForm
from services.cart_service import CartService
from services.nowpayments_service import NOWPaymentsService
from apps.payments.models import Payment
from core.utils import is_htmx

def checkout(request):
    cart = CartService.get_cart_from_session(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        if is_htmx(request):
            response = HttpResponse()
            response['HX-Redirect'] = reverse('product_list') # Redirect to catalog? Or somewhere else
            return response
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.subtotal = cart.total_price
                    order.total = order.subtotal + order.shipping_cost
                    
                    # Ensure unique order number generation if not handled by signal/save override safely
                    # The model save method handles it, so allow it.
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
                    
                    # Create Payment Invoice immediately
                    invoice_data = NOWPaymentsService.create_invoice(order)
                    
                    Payment.objects.create(
                        order=order,
                        payment_id=invoice_data.get('id'),
                        payment_status='waiting',
                        price_amount=invoice_data.get('price_amount'),
                        price_currency=invoice_data.get('price_currency'),
                    )

                    CartService.clear_cart(request)
                    
                    invoice_url = invoice_data.get('invoice_url')
                    
                    if is_htmx(request):
                        # Force browser redirect to external payment page
                        response = HttpResponse()
                        response['HX-Redirect'] = invoice_url
                        return response
                    
                    return redirect(invoice_url)
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f"An error occurred: {e}")
        else:
            for error in form.errors.values():
                 messages.error(request, error)
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart': cart,
        'cart_total': cart.total_price,
        'is_htmx': is_htmx(request)
    }
    
    if is_htmx(request):
         return render(request, 'orders/partials/checkout_content.html', context)
         
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    context = {'order': order, 'is_htmx': is_htmx(request)}
    
    if is_htmx(request):
        return render(request, 'orders/partials/confirmation_content.html', context)
        
    return render(request, 'orders/confirmation.html', context)

