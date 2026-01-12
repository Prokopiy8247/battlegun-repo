from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_status', 'price_amount', 'price_currency', 'created_at')
    list_filter = ('payment_status', 'created_at', 'price_currency')
    search_fields = ('payment_id', 'order__order_number', 'pay_address')
    readonly_fields = ('created_at', 'updated_at')
