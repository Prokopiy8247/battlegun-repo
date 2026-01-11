from apps.cart.models import Cart, CartItem
from apps.catalog.models import Product

class CartService:
    @staticmethod
    def get_cart_from_session(request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_key=session_key)
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
