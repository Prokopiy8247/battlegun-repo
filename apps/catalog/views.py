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
        products = products.filter(power_supply__in=power_supplies)

    # Filter by Manufacturer
    manufacturers = request.GET.getlist('manufacturer')
    if manufacturers:
        products = products.filter(brand__in=manufacturers)

    # Constants for filtering
    ALL_POWER_SUPPLIES = ['Gas', 'Spring', 'AEG']
    ALL_MANUFACTURERS = [
        'SPECNA ARMS', 'GOLDEN EAGLE', 'DOUBLE BELL', 'CYMA', 'A&K', 
        'ARCTURUS', 'E&C', 'UMAREX', 'SRC', 'NUPROL'
    ]

    context = {
        'products': products,
        'current_category': current_category,
        'all_power_supplies': ALL_POWER_SUPPLIES,
        'all_manufacturers': ALL_MANUFACTURERS,
        'selected_power_supplies': power_supplies,
        'selected_manufacturers': manufacturers,
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
