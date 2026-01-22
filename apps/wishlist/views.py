
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from apps.wishlist.models import WishlistItem
from apps.catalog.models import Product

def _get_wishlist_query(request):
    if request.user.is_authenticated:
        return WishlistItem.objects.filter(user=request.user)
    
    if not request.session.session_key:
        request.session.save()
    return WishlistItem.objects.filter(session_key=request.session.session_key)

def _get_wishlist_count(request):
    return _get_wishlist_query(request).count()

def wishlist_list(request):
    wishlist_items = _get_wishlist_query(request).select_related('product').prefetch_related('product__images')
    context = {
        'wishlist_items': wishlist_items,
    }
    
    # Check for HTMX request targeting main-content
    if request.headers.get('HX-Request') == 'true' and request.headers.get('HX-Target') == 'main-content':
        return render(request, 'wishlist/partials/wishlist_body.html', context)
        
    return render(request, 'wishlist/wishlist_list.html', context)

@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Toggle logic
    if request.user.is_authenticated:
        obj, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.delete()
            in_wishlist = False
        else:
            in_wishlist = True
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        
        obj, created = WishlistItem.objects.get_or_create(session_key=session_key, product=product)
        if not created:
            obj.delete()
            in_wishlist = False
        else:
            in_wishlist = True
            
    # Button Context
    context = {
        'product': product,
        'in_wishlist': in_wishlist,
    }
    
    # Render Button
    button_html = render_to_string('wishlist/partials/wishlist_button.html', context, request)
    
    # Render Header Count (OOB)
    count = _get_wishlist_count(request)
    count_html = render_to_string('wishlist/partials/wishlist_count.html', {'wishlist_count': count}, request)
    
    return HttpResponse(button_html + count_html)

@require_POST
def remove_wishlist_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        WishlistItem.objects.filter(user=request.user, product=product).delete()
    else:
        if request.session.session_key:
            WishlistItem.objects.filter(session_key=request.session.session_key, product=product).delete()
            
    # Return empty string to remove the row, AND trigger count update OOB
    count = _get_wishlist_count(request)
    count_html = render_to_string('wishlist/partials/wishlist_count.html', {'wishlist_count': count}, request)
    
    return HttpResponse(count_html)
