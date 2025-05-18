from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .cart import Cart as SessionCart
from app.models import Crop, Cart, CartItem, Order, OrderItem, Customer
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
import json
from app.forms import CustomerForm
from app.views import update_profile,view_profile
from payments.forms import PaymentForm


@login_required
def my_orders(request):
    """Fetch and display all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')  # Orders sorted by most recent
   
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """Fetch and display details for a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


def checkout(request):
    cart = SessionCart(request)
    cart_items = cart.get_crops()  # This returns all crops in the cart
    quantities = cart.get_quantities()
    
    # total_price = cart.cart_total()
    # Ensure that quantities and crops are valid
    quantities_dict = {int(key): value for key, value in quantities.items()}
    total_price= 0
   
    
    for crop in cart_items:
        total_price += crop.price_per_unit * quantities_dict.get(crop.id, 0)
    
    transport_fee =  cart.get_transport_fee() 
    grand_total = total_price + transport_fee
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'quantities': quantities_dict,
        'total_price': total_price, 
        'transport_fee': transport_fee,
        'grand_total': grand_total,
        
    })



@transaction.atomic
def place_order(request):
    try:
        # Get the active cart for the user
        # cart = Cart.objects.get(user=request.user, active=True)
        cart = SessionCart(request)
        cart_items = cart.get_crops()

        if not cart_items:
            print( "Your cart is empty.")
            return redirect('cart_summary')

        transport_fee = cart.get_transport_fee() 
        total_price = cart.get_total_price()

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price= total_price,
            transport_fee=transport_fee,
            payment_method=request.POST.get('payment_method', 'COD'),  # Default to COD
            delivery_address=request.POST.get('delivery_address', 'No address provided'),
        )

        # Transfer cart items to order items
        for item in cart_items:
            crop_quantity = cart.get_quantities().get(str(item.id), 0)

            if item.quantity >= crop_quantity:
                # Reduce crop quantity
                item.quantity -= crop_quantity
                if item.quantity == 0:
                    messages.warning(request, f"{item.crop_name} is now Out of Stock.")
                item.save()
            else:
                messages.warning(request, f"Not enough stock for {item.crop_name}. Only {item.quantity} available.")


            OrderItem.objects.create(
                order=order,
                crop=item,
                user=request.user,
                quantity=cart.get_quantities().get(str(item.id), 0),
                price_per_unit=item.price_per_unit,
            )

            
        # clear the session cart after placing the order
        request.session['session_key'] = {} # Reset the cart in the session

        # Debugging print statements
        print(f"Order ID: {order.id}")
        messages.success(request, "Your order has been placed successfully!")

        # Redirect to order confirmation page with the order ID
        print(f"Redirecting to order confirmation for Order ID: {order.id}")
        return redirect('order_confirmation', order_id=order.id)

    except Cart.DoesNotExist:
        print( "You don't have an active cart.")
        return redirect('customer_dashboard')

    except Exception as e:
        print(f"Error occurred in place_order: {e}")
        messages.error(request, f"An error occurred: {e}")
        return redirect('cart_summary')



def order_confirmation(request, order_id):
    # Fetch the specific order for the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # order_items = order.items.all()  # Get all related OrderItems
    order_items = OrderItem.objects.filter(order = order)
    total_price = order.total_price
    transport_fee = order.transport_fee
    grand_total = total_price + transport_fee

    context = {
        "order": order,
        "order_items": order_items,
        "total_price": total_price,
        "transport_fee": transport_fee,
        "grand_total": grand_total,
    }
    return render(request, "order_confirmation.html", context)



def cart_summary(request):
    cart = SessionCart(request)
    cart_items = cart.get_crops()  # This returns all crops in the cart
    quantities = cart.get_quantities()
    
    # total_price = cart.cart_total()
    # Ensure that quantities and crops are valid
    quantities_dict = {str(key): value for key, value in quantities.items()}
    item_prices_dict = {}

      # Calculate total price for each item and overall total
    total_price = 0
    for crop in cart_items:
        # Use str(crop.id) to match the quantities_dict keys
        crop_quantity = quantities_dict.get(str(crop.id), 0)
        item_total = crop.price_per_unit * crop_quantity
        item_prices_dict[crop.id] = item_total
        total_price += item_total  # Add to total cart price

    # for crop in cart_items:
    #     item_prices_dict[crop.id] = crop.price_per_unit * quantities_dict.get(str(crop.id),0)

    # total_price = sum(item_prices_dict.values())  # Calculate total price of all crops
    
    print("Cart Items: ",cart_items)
    print("Quantities: ",quantities)
    print("Total Price: ",total_price)
    print("Item Prices: ",item_prices_dict)


    return render(request, 'cart_summary.html', {
        'cart_items': cart_items,
        'quantities': quantities_dict,
        'total_price': total_price, 
        'item_prices': item_prices_dict,
        
    })


def cart_add(request):
    cart = SessionCart(request)  # Use the session-based Cart
    if request.POST.get('action') == 'post':
        crop_id = int(request.POST.get('crop_id'))
        crop_qty = int(request.POST.get('crop_qty'))
        # cart = request.session.get('cart', [])
        crop = get_object_or_404(Crop, id=crop_id)

        # print("Cart items before adding:", cart.get_crops())  # To see if the cart is properly initialized

         # Check stock availability
        if crop.quantity < crop_qty:
            return JsonResponse({
                'error': f"Only {crop.quantity} {crop.unit} of {crop.crop_name} available."
            }, status=400)

        # Check if the crop is already in the cart and ensure it doesn't exceed stock
        current_cart_quantity = cart.get_quantities().get(str(crop.id), 0)
       
        if current_cart_quantity + crop_qty > crop.quantity:
            return JsonResponse({
                'error': f"Adding this quantity exceeds the available stock. Current available: {crop.quantity - current_cart_quantity} {crop.unit}."
            }, status=400)




        # Add crop to the session cart
        cart.add(crop=crop, quantity=crop_qty, user=request.user)
        
        print("Cart items after adding to session:", request.session.get('session_key',{}))


        # Get total quantity of unique items in the cart
        cart_quantity = len(cart)

        #total price for specific crop
        item_total = cart.get_item_total(crop_id)
      
        # Calculate the total price for the added crop
        total_price = cart.get_total_price()
 
        # request.session.modified = True


        return JsonResponse({
            'qty': cart_quantity, 
            'item_total':item_total,
            'total_price': total_price
            })


       
def cart_update(request):
    cart = SessionCart(request)  # Use the session-based Cart implementation

    if request.method == 'POST':
        crop_id = (request.POST.get('crop_id'))
        crop_qty = int(request.POST.get('crop_qty'))

        
        # Update the quantity in the cart
        cart.update(crop=crop_id, quantity=crop_qty)

        # Calculate total price for this specific crop
        item_total = cart.get_item_total(crop_id)
        # item = Crop.objects.get(id=crop_id)
        # item_total = item.price_per_unit * crop_qty
        # Recalculate the total cart price
        total_price = cart.get_total_price()

        # Return the updated totals as JSON
        return JsonResponse({
            'item_total': item_total,
            'total_price': total_price
        })
    
    return JsonResponse({'error': 'Invalid request method or missing action'}, status=400)
   


def cart_delete(request):
    cart = SessionCart(request)
    if request.method == "POST":
    # if request.POST.get('action') == 'post':
        crop_id = int(request.POST.get('crop_id'))  # Get crop_id from POST data
        
        if crop_id:
            crop_id=int(crop_id)

            cart.delete(crop = crop_id, user = request.user)

        # Recalculate the total price for the entire cart
            total_price = cart.get_total_price()

            return JsonResponse({
                'crop' : crop_id ,
                'total_price' : total_price
            })
        
        return JsonResponse({'error': 'Missing crop_id'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)