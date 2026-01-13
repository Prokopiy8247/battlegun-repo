import logging
from services.cart_service import CartService

logger = logging.getLogger(__name__)

def cart(request):
    try:
        cart = CartService.get_cart_from_session(request)
        # logger.info(f"Context Processor Cart: {cart} ID: {cart.id} Items: {cart.total_items}")
        return {'cart': cart}
    except Exception as e:
        logger.error(f"Error in cart context processor: {e}")
        return {'cart': None}
