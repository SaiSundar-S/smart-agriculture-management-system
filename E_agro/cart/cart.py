from app.models import Crop,Customer
import json


class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        if 'session_key' not in self.session:
            self.session['session_key'] = {}  # Initialize cart if not present
        self.cart = self.session['session_key']


    def db_add(self,crop,quantity,user):
        crop_id = str(crop)
        
        if crop_id in self.cart:
            self.cart[crop_id] += quantity  # Add to existing quantity if item exists
        else:
            self.cart[crop_id] = quantity  # Add new item
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.get(user = user)
            # cart_data = str(self.cart).replace("\'" , "\"")
            # current_user.update(cart = cart_data)
            cart_data = json.dumps(self.cart)
            current_user.old_cart = cart_data
            current_user.save()



    def add(self,crop, quantity,user):
        crop_id = str(crop.id)
        crop_qty = str(quantity)
        
        if crop_id in self.cart:
            self.cart[crop_id] += int(crop_qty)  # Add to existing quantity if item exists
        else:
            self.cart[crop_id] = int(crop_qty)  # Add new item
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.get(user = user)
            # cart_data = str(self.cart).replace("\'" , "\"")
            # current_user.update(cart = cart_data)
            cart_data = json.dumps(self.cart)
            current_user.old_cart = cart_data
            current_user.save()

        return self.cart
    
        
    def get_crops(self):
        crop_ids = self.cart.keys()
        crops = Crop.objects.filter(id__in=crop_ids)
        return crops

    def get_quantities(self):
        return self.cart
    
    def __len__(self):
        return len(self.cart)

    def delete(self, crop , user):
        crop_id = str(crop)
        if crop_id in self.cart:
            del self.cart[crop_id]
            self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Customer.objects.get(user = user)
            # cart_data = str(self.cart).replace("\'" , "\"")
            # current_user.update(cart = cart_data)
            cart_data = json.dumps(self.cart)
            current_user.old_cart = cart_data
            current_user.save()

        return self.cart
       
    # def clear(self):
    #     self.session['session_key'] = {}
    #     self.session.modified = True
    
    def clear(self):
        """ Clear the cart from the session """
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session['session_key'] = self.cart  # Save cart back to the session
        self.session.modified = True

    def update(self, crop, quantity):
        crop_id = str(crop)
        if crop_id in self.cart:
            self.cart[crop_id] = quantity
            self.save()
        self.session.modified = True
        return (self.cart, self.get_total_price)

    def get_item_total(self, crop_id):
        if crop_id in self.cart:
            try:
                crop = Crop.objects.get(id=int(crop_id))
                quantity = self.cart[crop_id]
                return crop.price_per_unit * quantity
            except Crop.DoesNotExist:
                return 0
        return 0

    def get_total_price(self):
        total_price = 0
        for crop_id, quantity in self.cart.items():
            try:
                crop = Crop.objects.get(id=int(crop_id))
                total_price += crop.price_per_unit * quantity
            except Crop.DoesNotExist:
                continue
        return total_price
    
    def get_transport_fee(self):
        return 100 #fixed transport fee
    
    def sync_cart_with_user(self, user):
        if self.request.user.is_authenticated:
            current_user = Customer.objects.get(user=user)
            if current_user.old_cart:
                # self.cart = json.loads(current_user.old_cart)
                # self.save()
                user_cart = json.loads(current_user.old_cart)

                # Merge session and database cart
                for crop_id, quantity in self.cart.items():
                    if crop_id in user_cart:
                        user_cart[crop_id] += quantity
                    else:
                        user_cart[crop_id] = quantity
                
                # Save merged cart to session and database
                self.cart = user_cart
                self.save()
                current_user.old_cart = json.dumps(self.cart)
                current_user.save()

