from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from app.models import CartItem, Cart, Crop, Order
import logging

logger = logging.getLogger(__name__)

@receiver(user_logged_out)
def save_cart_on_logout(sender, request, user, **kwargs):
    
    if user is None:  # Ensure user is not None
        logger.warning("No authenticated user found during logout.")
        return  # Exit if user is None
    
    
    logger.info(f"User {user.username} logged out, saving cart.")
    session_cart = request.session.get('cart', {})

    if user.is_authenticated:
        logger.info(f"Session Cart: {session_cart}")
        cart, created = Cart.objects.get_or_create(user=user, active=True)

        for crop_id, quantity in session_cart.items():
            try:
                crop = Crop.objects.get(id=crop_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, crop=crop)
                cart_item.quantity = quantity
                cart_item.save()
                logger.info(f"Saved cart item: {crop.crop_name} x {quantity}")
            except Crop.DoesNotExist:
                logger.warning(f"Crop with ID {crop_id} not found.")
            
        request.session['cart'] = {}  # Clear session cart
    
         # Save orders (if any)
        try:
            orders = Order.objects.filter(user=user, status='pending')  # Adjust the condition as necessary
            for order in orders:
                order.save()  # Save any changes to pending orders, if necessary
                logger.info(f"Pending order {order.id} saved for user {user.username}.")
        except Order.DoesNotExist:
            logger.warning(f"No pending orders found for user {user.username}.")
    
    
    else:
        logger.warning("User is not authenticated, cart not saved.")

@receiver(user_logged_in)
def sync_cart_on_login(sender, request, user, **kwargs):
    session_cart = request.session.get('cart', {})

    if user.is_authenticated:
        db_cart_items = CartItem.objects.filter(cart__user=user, cart__active=True)

        for cart_item in db_cart_items:
            session_cart[cart_item.crop.id] = cart_item.quantity

        request.session['cart'] = session_cart

        # Sync orders (if any) for the user
        orders = Order.objects.filter(user=user, status='pending')  # Adjust as necessary
        for order in orders:
            # Example logic: You might want to sync the order details to the session or show in the UI
            logger.info(f"Found pending order {order.id} for user {user.username}.")

    else:
        logger.warning("User is not authenticated, cart and orders not synced.")
