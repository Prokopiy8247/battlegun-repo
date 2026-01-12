from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'email', 'get_payment_id', 'first_name', 'last_name', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at', 'country')
    search_fields = ('order_number', 'email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('order_number', 'get_payment_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 20

    def get_payment_id(self, obj):
        if hasattr(obj, 'payment'):
            return obj.payment.payment_id
        return '-'
    get_payment_id.short_description = 'Payment ID'
