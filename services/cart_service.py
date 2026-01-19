from django.db.models import Prefetch
from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product

class CartService:
    @staticmethod
    def get_cart_from_session(request):
        user = request.user if request.user.is_authenticated else None
        
        if user:
            # User authenticated: get or create user cart
            try:
                cart = Cart.objects.prefetch_related(
                    Prefetch('items', queryset=CartItem.objects.select_related('product').prefetch_related('product__images'))
                ).get(user=user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=user)
        else:
            # User anonymous: get or create session cart
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            
            try:
                cart = Cart.objects.prefetch_related(
                    Prefetch('items', queryset=CartItem.objects.select_related('product').prefetch_related('product__images'))
                ).get(session_key=session_key)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(session_key=session_key)
                
        return cart

    @staticmethod
    def add_to_cart(request, product_id, quantity=1):
        cart = CartService.get_cart_from_session(request)
        product = Product.objects.get(pk=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.price, 'quantity': 0}
        )
        
        # Determine price (use discount if available)
        current_price = product.discount_price if product.discount_price else product.price
        
        # Update price to current
        cart_item.price = current_price
        cart_item.quantity += int(quantity)
        cart_item.save()
        
        # Update cart timestamp
        cart.save()
        return cart

    @staticmethod
    def remove_from_cart(request, item_id):
        cart = CartService.get_cart_from_session(request)
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
            item.delete()
            cart.save()
        except CartItem.DoesNotExist:
            pass
        return cart
        
    @staticmethod
    def update_quantity(request, item_id, quantity):
        cart = CartService.get_cart_from_session(request)
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
            if int(quantity) > 0:
                item.quantity = int(quantity)
                item.save()
            else:
                item.delete()
            cart.save()
        except CartItem.DoesNotExist:
            pass
        return cart

    @staticmethod
    def clear_cart(request):
         cart = CartService.get_cart_from_session(request)
         cart.items.all().delete()
         cart.save()

    @staticmethod
    def merge_carts_after_login(request, old_session_key, user):
        """
        Merges the anonymous session cart (old_session_key) into the authenticated user's cart.
        """
        if not old_session_key or not user:
            return

        try:
            # Try to get the old anonymous cart
            anon_cart = Cart.objects.prefetch_related('items').get(session_key=old_session_key, user__isnull=True)
        except Cart.DoesNotExist:
            return

        # Get or create the user's permanent cart
        try:
            user_cart = Cart.objects.prefetch_related('items').get(user=user)
        except Cart.DoesNotExist:
            # If user has no cart, simply convert the anon cart to user cart
            anon_cart.user = user
            anon_cart.session_key = None 
            anon_cart.save()
            return

        # If both exist, merge items from anon_cart to user_cart
        for anon_item in anon_cart.items.all():
            existing_item = user_cart.items.filter(product=anon_item.product).first()
            if existing_item:
                existing_item.quantity += anon_item.quantity
                existing_item.save()
            else:
                anon_item.cart = user_cart
                anon_item.save()
        
        # Delete the old anonymous cart container since items moved
        anon_cart.delete()
