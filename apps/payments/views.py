import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.orders.models import Order
from .models import Payment
from services.nowpayments_service import NOWPaymentsService
from services.tasks import send_payment_success_email



@csrf_exempt
@require_POST
def webhook(request):
    # Verify signature
    sig = request.headers.get('x-nowpayments-sig')
    if not sig:
        return HttpResponseBadRequest("Missing Signature")

    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    # Verify validity
    if not NOWPaymentsService.check_signature(body_data, sig):
         return HttpResponseBadRequest("Invalid Signature")

    # Process payment
    # data contains: payment_status, payment_id, order_id, etc.
    payment_status = body_data.get('payment_status')
    order_id = body_data.get('order_id') # This is our UUID string
    
    if order_id:
        try:
            # We look for the Payment associated with this order
            order = Order.objects.get(id=order_id)
            payment = getattr(order, 'payment', None)
            
            if payment:
                payment.payment_status = payment_status
                payment.pay_amount = body_data.get('pay_amount')
                payment.pay_currency = body_data.get('pay_currency')
                payment.pay_address = body_data.get('pay_address')
                payment.save()
                
                # Update order status based on payment status
                if payment_status == 'finished' or payment_status == 'confirmed':
                    if order.status != 'paid':
                        order.status = 'paid'
                        order.save()
                        # Send payment success email asynchronously
                        send_payment_success_email.delay(order.id)
                elif payment_status == 'failed':
                    order.status = 'cancelled' # or failed
                    order.save()
                    
        except Order.DoesNotExist:
            pass
            
    return HttpResponse("OK")

def payment_waiting(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'payments/waiting.html', {'order': order})

def payment_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'payments/success.html', {'order': order})

def payment_failed(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'payments/failed.html', {'order': order})

