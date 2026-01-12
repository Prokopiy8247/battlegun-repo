import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.orders.models import Order
from .models import Payment
from services.nowpayments_service import NOWPaymentsService

def payment_start(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/start.html', {'order': order})

@require_POST
def create_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    try:
        # Create invoice via service
        invoice_data = NOWPaymentsService.create_invoice(order)
        
        # Create Payment record
        # invoice_data should contain: id, order_id, price_amount, price_currency, invoice_url, etc.
        # Note: 'id' in invoice_data is the NOWPayments invoice ID.
        
        Payment.objects.create(
            order=order,
            payment_id=invoice_data.get('id'),
            payment_status='waiting',
            price_amount=invoice_data.get('price_amount'),
            price_currency=invoice_data.get('price_currency'),
            # invoice_url=invoice_data.get('invoice_url') # We don't have a field for this in tech.md, strictly 6.9
        )
        
        return redirect(invoice_data.get('invoice_url'))
    
    except Exception as e:
        return render(request, 'payments/error.html', {'error': str(e), 'order': order})

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
    np_id = body_data.get('payment_id')

    # Update Payment
    # We might need to look up by payment_id or order_id
    # order_id in payload matches our order.id (str)
    
    if order_id:
        try:
            # We look for the Payment associated with this order
            # Or by payment_id if we stored the invoice id as payment_id differently?
            # In create_payment we stored invoice ID as payment_id.
            # IPN for invoice might send invoice ID or payment ID.
            # Usually IPN sends payment ID (different from invoice ID) if it's a payment update?
            # NOWPayments docs: "The body of the request is similiar to a get payment status response body."
            # "parent_payment_id"?
            
            # Let's try to find payment by order first
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
                    order.status = 'paid'
                    order.save()
                elif payment_status == 'failed':
                    order.status = 'cancelled' # or failed
                    order.save()
                    
        except Order.DoesNotExist:
            pass
            
    return HttpResponse("OK")
