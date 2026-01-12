from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from apps.orders.models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_order_created_email(order_id):
    """
    Sends an email to the customer when an order is created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order Confirmation - {order.order_number}'
        message = f"Dear {order.first_name},\n\nYour order {order.order_number} has been created successfully.\nPlease proceed with the payment to complete your order.\n\nThank you!"
        
        # In a real app, we'd use a HTML template
        # html_message = render_to_string('emails/order_created.html', {'order': order})
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
        logger.info(f"Order created email sent to {order.email} for order {order.order_number}")
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found for sending email.")
    except Exception as e:
        logger.error(f"Failed to send order created email for order {order_id}: {e}")

@shared_task
def send_payment_success_email(order_id):
    """
    Sends an email to the customer when payment is successful (receipt).
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Payment Receipt - {order.order_number}'
        
        payment_info = ""
        if hasattr(order, 'payment'):
             payment_info = f"Amount Paid: {order.payment.price_amount} {order.payment.price_currency}\nPayment Status: {order.payment.payment_status}"

        message = f"Dear {order.first_name},\n\nWe have received your payment for order {order.order_number}.\n\n{payment_info}\n\nYour order is now being processed.\n\nThank you for shopping with us!"
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
        logger.info(f"Payment success email sent to {order.email} for order {order.order_number}")
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found for sending payment email.")
    except Exception as e:
        logger.error(f"Failed to send payment success email for order {order_id}: {e}")
