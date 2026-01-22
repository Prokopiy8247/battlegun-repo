from django import template
from django.conf import settings
from decimal import Decimal

register = template.Library()

@register.filter(name='currency')
def currency(value, request=None):
    """
    Converts a price in the base currency (EUR) to the selected currency.
    Usage: {{ product.price|currency:request }}
    """
    if value is None:
        return ""
        
    try:
        # Check if value is a string that looks like a number
        value = Decimal(str(value))
    except (ValueError, TypeError):
        return value

    # If no request is passed, default to EUR
    if not request:
         return f"{value:.2f} €"

    currency_code = request.session.get('currency', settings.DEFAULT_CURRENCY)
    
    if currency_code == settings.DEFAULT_CURRENCY:
        return f"{value:.2f} €"
    
    rate = settings.EXCHANGE_RATES.get(currency_code, 1)
    # Convert to Decimal to ensure precision
    converted_value = value * Decimal(str(rate))
    
    symbol = settings.CURRENCIES.get(currency_code, {}).get('symbol', currency_code)
    
    return f"{converted_value:.2f} {symbol}"

@register.inclusion_tag('core/partials/currency_selector.html', takes_context=True)
def currency_selector(context):
    request = context.get('request')
    currency_code = settings.DEFAULT_CURRENCY
    if request:
        currency_code = request.session.get('currency', settings.DEFAULT_CURRENCY)
    
    currency_symbol = settings.CURRENCIES.get(currency_code, {}).get('symbol', '€')
    
    return {
        'request': request,
        'currency_code': currency_code,
        'currency_symbol': currency_symbol,
        'currencies': settings.CURRENCIES,
        'csrf_token': context.get('csrf_token'),  # We need to pass csrf_token explicitly or use takes_context
    }
