
from apps.wishlist.models import WishlistItem

def wishlist_count(request):
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        if request.session.session_key:
            count = WishlistItem.objects.filter(session_key=request.session.session_key).count()
        else:
            count = 0
            
    return {'wishlist_count': count}
