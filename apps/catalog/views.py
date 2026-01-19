from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.db.models import Q
from .models import Product, Category

def is_htmx(request):
    return request.headers.get('HX-Request') == 'true'

def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True).order_by('-created_at').prefetch_related('images')
    current_category = None
    
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Filter by Power Supply
    power_supplies = request.GET.getlist('power_supply')
    if power_supplies:
        products = products.filter(power_supply_en__in=power_supplies)

    # Filter by Manufacturer
    manufacturers = request.GET.getlist('manufacturer')
    if manufacturers:
        products = products.filter(brand__in=manufacturers)

    # Constants for filtering
    from django.utils.translation import gettext as _
    ALL_POWER_SUPPLIES = [
        {'value': 'Gas/CO2', 'label': _('Gas')},
        {'value': 'Spring', 'label': _('Spring')},
        {'value': 'AEG', 'label': _('AEG')},
    ]
    ALL_MANUFACTURERS = [
        'SPECNA ARMS', 'GOLDEN EAGLE', 'DOUBLE BELL', 'CYMA', 'A&K', 
        'ARCTURUS', 'E&C', 'UMAREX', 'SRC', 'NUPROL'
    ]

    # Wishlist IDs
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = list(request.user.wishlist.values_list('product_id', flat=True))
    elif request.session.session_key:
        from apps.wishlist.models import WishlistItem
        wishlist_product_ids = list(WishlistItem.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True))

    context = {
        'products': products,
        'current_category': current_category,
        'all_power_supplies': ALL_POWER_SUPPLIES,
        'all_manufacturers': ALL_MANUFACTURERS,
        'selected_power_supplies': power_supplies,
        'selected_manufacturers': manufacturers,
        'wishlist_product_ids': wishlist_product_ids,
    }

    if is_htmx(request):
        header_target = request.headers.get('HX-Target')
        if header_target == 'main-content':
             return render(request, 'catalog/partials/product_list_body.html', context)
        elif header_target == 'category-grid':
             return render(request, 'catalog/partials/product_list_content.html', context)
    
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }

    if is_htmx(request) and request.headers.get('HX-Target') == 'main-content':
        return render(request, 'catalog/partials/product_detail_body.html', context)

    return render(request, 'catalog/product_detail.html', context)

def home(request):
    # For now, home redirects to catalog or renders catalog as home
    return product_list(request)


    return product_list(request)
