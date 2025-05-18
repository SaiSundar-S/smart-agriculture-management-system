from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import FarmerRegistrationForm, CustomerRegistrationForm, CropForm, ALLUserProfileForm, FarmerForm, CustomerForm
from .models import  Farmer, Customer, Crop, Cart, Address, CartItem, Order, ALLUserProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .serializers import AddressSerializer
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib import messages
import json
from cart.cart import Cart




# Home page view
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('e_agro:home') 


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', None)
                # Check if the user is a farmer or customer and redirect accordingly
                try:
                    # Check if the user has a related farmer profile
                    farmer_profile = Farmer.objects.get(user=user)
                    return redirect(next_url or 'e_agro:farmer_dashboard')
                except Farmer.DoesNotExist:
                    # If no farmer profile exists, assume customer and redirect to their dashboard
                    current_user = Customer.objects.get(user__id = request.user.id)
                    saved_cart = current_user.old_cart
                    if saved_cart:
                        converted_cart = json.loads(saved_cart)
                        cart= Cart(request)
                        for key,value in converted_cart.items():
                            cart.db_add(crop=key, quantity= value , user= request.user )


                    return redirect(next_url or 'e_agro:customer_dashboard')  # Redirect to Customer Dashboard
    else:
        form = AuthenticationForm()
    
    return render(request, 'agro_login.html', {'form': form}) 

def register_farmer(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Farmer profile linked to the user
            Farmer.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                farm_name=form.cleaned_data.get('farm_name'),
                farm_location=form.cleaned_data.get('farm_location'),
                phone_number=form.cleaned_data.get('phone_number'),
            )
            # Automatically log in the user after registration
            login(request, user)
            return redirect('e_agro:farmer_dashboard')
    else:
        form = FarmerRegistrationForm()
    
    return render(request, 'register_farmer.html', {'form': form})

# Customer registration view
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                phone_number=form.cleaned_data.get('phone_number'),
                email=form.cleaned_data.get('email'),
                address = form.cleaned_data.get('address')
            )
            login(request, user)
            return redirect('e_agro:customer_dashboard')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})



@login_required
def update_profile(request):
    user = request.user

    # Try to get Farmer or Customer associated with the user
    try:
        farmer = Farmer.objects.get(user=user)
    except Farmer.DoesNotExist:
        farmer = None

    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        # Forms for updating the user and farmer/customer profiles
        user_form = ALLUserProfileForm(request.POST, instance=user)

        # Only set profile_form for farmer or customer
        if farmer:
            profile_form = FarmerForm(request.POST, instance=farmer)
        elif customer:
            profile_form = CustomerForm(request.POST, instance=customer)
        else:
            profile_form = None

        # Validate forms
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save user details
            profile_form.save()  # Save farmer/customer details

            messages.success(request, 'Your profile has been updated successfully!')
            
            # Redirect to the dashboard to reflect updated details
            return redirect('e_agro:view_profile')  # Redirect to the dashboard page
        else:
            messages.error(request, 'There was an error updating your profile. Please check the details and try again.')
    else:
        # Initialize forms with existing data
        user_form = ALLUserProfileForm(instance=user)

        if farmer:
            profile_form = FarmerForm(instance=farmer)
        elif customer:
            profile_form = CustomerForm(instance=customer)
        else:
            profile_form = None

    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_farmer': bool(farmer),
        'is_customer': bool(customer),
    })

@login_required
def view_profile(request):
    user = request.user

    try:
        farmer = Farmer.objects.get(user=user)
    except Farmer.DoesNotExist:
        farmer = None

    try:
        customer = Customer.objects.get(user=user)

    except Customer.DoesNotExist:
        customer = None

    return render(request, 'view_profile.html', {
        'user': user,
        'farmer': farmer,
        'customer': customer,
       
    })


@login_required
def farmer_dashboard(request):
    try:
        # Get the farmer profile and associated crops
        farmer = request.user.farmer
        
        # Start the query to filter crops
        crops = Crop.objects.filter(farmer=farmer)
        
        # Apply category filter
        category = request.GET.get('category')
        if category:
            crops = crops.filter(category__iexact=category)
        
        # Apply stock (quantity) filter
        quantity_range = request.GET.get('quantity_range')
        # if quantity_range:
        if quantity_range == 'asc':
                crops = crops.order_by('quantity')  # Low to High
        elif quantity_range == 'desc':
                crops = crops.order_by('-quantity')  # High to Low
        

         # Filter by price range
        price_range = request.GET.get('price_range')
        if price_range == 'asc':
            crops = crops.order_by('price_per_unit')
        elif price_range == 'desc':
            crops = crops.order_by('-price_per_unit')


        # Apply price range filter
        # price_min = request.GET.get('price_min')
        # price_max = request.GET.get('price_max')
        # if price_min:
        #     crops = crops.filter(price_per_unit__gte=price_min)
        # if price_max:
        #     crops = crops.filter(price_per_unit__lte=price_max)

        # crops = crops.order_by('-created_at')  # Optional: order by date
        
        # Add stock status for each crop (Out of Stock if quantity is 0)
        crops_with_stock_status = []
        for crop in crops:
            if crop.quantity == 0:
                stock_status = 'Out of Stock'
            else:
                stock_status = f'In Stock ({crop.quantity})'
            
            crops_with_stock_status.append({
                'crop': crop,
                'stock_status': stock_status
            })

    except Farmer.DoesNotExist:
        return redirect('e_agro:register_farmer')  # Or handle appropriately
    
    return render(request, 'farmer_dashboard.html', {'farmer': farmer, 'crops': crops})


def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = request.user.farmer
            crop.save()
            return redirect('e_agro:farmer_dashboard')
    else:
        form = CropForm()
    
    return render(request, 'add_crop.html', {'form': form})

def edit_crop(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()

            # Update stock status (display Out of Stock if quantity is 0)
            if crop.quantity == 0:
                crop.status = 'Out of Stock'
            else:
                crop.status = 'In Stock'
            
            crop.save()  # Save the updated crop with the new stock status

            return redirect('e_agro:farmer_dashboard')
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'edit_crop.html', {'form': form, 'crop': crop})

def delete_crop(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
    crop.delete()
    return redirect('e_agro:farmer_dashboard')

#customers dashboard 
@login_required
def customer_dashboard(request):
    crops = Crop.objects.all()

    # Handle search functionality
    query = request.GET.get('q', '').strip()
    if query:
        crops = crops.filter(crop_name__icontains=query)

    # Handle category filter
    category = request.GET.get('category', '').strip().lower()
    if category:
        crops = crops.filter(category__iexact=category)

    crops_per_page = 9
    paginator = Paginator(crops, crops_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

     # Get the customer object
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None

    cart_items = request.session.get('cart', [])


    return render(request, 'customer_dashboard.html', {
        'page_obj': page_obj,
        'customer':customer,
        'cart_items': cart_items,
    })



# View for Crop Detail
def crop_detail(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    return render(request, 'crop_detail.html', {'crop': crop})



# Function to get the cart from the session
def get_cart(request):
    cart = request.session.get('cart', {})
    total_price = 0
    transport_fee = 100  # Fixed transport fee, or can be dynamic
    # Iterate over each item in the cart and calculate the total price
    for item in cart.values():
        item_price = item.get('price', 0)
        item_quantity = item.get('quantity', 0)
        total_price += item_price * item_quantity  # Price * Quantity

    # Calculate grand total (total price + transport fee)
    # grand_total = total_price + transport_fee
    return cart, total_price

# # Add item to cart
# def add_to_cart(request, crop_id):
#     crop = Crop.objects.get(id=crop_id)
#     cart = request.session.get('cart', {})
#     if crop_id in cart:
#         cart[crop_id]['quantity'] += 1
#     else:
#         cart[crop_id] = {
#             'name': crop.crop_name,
#             'price': crop.price_per_unit,
#             'quantity': 1
#         }
#     request.session['cart'] = cart
#     return redirect('view_cart')

# @login_required
# def update_cart_quantity(request, cart_item_id, action):
#     """Handle cart item quantity update."""
#     # Get the cart item from the database
#     cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

#     # Update the quantity based on the action
#     if action == 'increase':
#         cart_item.quantity += 1
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1
#     else:
#         return JsonResponse({'error': 'Invalid action or quantity'}, status=400)

#     # Save the updated cart item
#     cart_item.save()

#     # Update the cart totals
#     cart = cart_item.cart
#     total_items = cart.total_items()
#     total_price = cart.total_price()

#     return JsonResponse({
#         'total_items': total_items,
#         'total_price': total_price,
#     })


@api_view(['GET'])
def get_addresses(request):
    """Retrieve all addresses for the logged-in customer."""
    customer = request.user.customer
    addresses = Address.objects.filter(customer=customer)
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_or_update_address(request):
    """Add or update a customer's address."""
    customer = request.user.customer
    address_data = request.data
    address_id = address_data.get('id')  # Check if updating an existing address

    if address_id:
        # Update existing address
        try:
            address = Address.objects.get(id=address_id, customer=customer)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=404)
        serializer = AddressSerializer(address, data=address_data, partial=True)
    else:
        # Create a new address
        serializer = AddressSerializer(data=address_data)

    if serializer.is_valid():
        serializer.save(customer=customer)
        return Response({'message': 'Address saved successfully', 'data': serializer.data})
    return Response(serializer.errors, status=400)