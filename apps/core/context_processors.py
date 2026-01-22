from django.conf import settings

def currency(request):
    """
    Context processor to add currency information to the template context.
    """
    currency_code = request.session.get('currency', settings.DEFAULT_CURRENCY)
    return {
        'currency_code': currency_code,
        'currency_symbol': settings.CURRENCIES.get(currency_code, {}).get('symbol', '€'),
        'currencies': settings.CURRENCIES,
        'na_text': "N/A",  # or gettext("N/A") if you want it translated
    }
