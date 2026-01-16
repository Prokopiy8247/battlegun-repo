from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponseRedirect

@require_POST
def set_currency(request):
    currency_code = request.POST.get('currency')
    next_url = request.POST.get('next', '/')
    
    # Validate currency code
    if currency_code in settings.CURRENCIES:
        request.session['currency'] = currency_code
    
    return HttpResponseRedirect(next_url)
