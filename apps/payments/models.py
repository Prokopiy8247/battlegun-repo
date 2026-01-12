import uuid
from django.db import models
from core.models import TimeStampedModel
from apps.orders.models import Order

class Payment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, related_name='payment', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True) # NOWPayments ID
    payment_status = models.CharField(max_length=50) # waiting, confirming, confirmed, sending, partially_paid, finished, failed, expired
    pay_address = models.CharField(max_length=200, blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=18, decimal_places=8, blank=True, null=True)
    pay_currency = models.CharField(max_length=10, blank=True, null=True)
    price_amount = models.DecimalField(max_digits=10, decimal_places=2)
    price_currency = models.CharField(max_length=10, default='usd')
    
    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_number}"
