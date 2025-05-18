from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ALLUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username



# Farmer Model
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) # Link with Django's built-in User model
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=150)
    email=models.EmailField(default="")
    farm_location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Crop(models.Model):

    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, related_name="crops")
    crop_name = models.CharField(max_length=100)
    crop_image = models.ImageField(upload_to='crop_images/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    CATEGORY_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('grain', 'Grain'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)  # Use choices for category
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('lb', 'Pound'),
    ]
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    transport_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set date when created

    def __str__(self):
        return f"{self.crop_name} by {self.farmer.user.username} ({self.quantity} {self.unit} at {self.price_per_unit}/{self.unit})"

    @property
    def total_price(self):
        return self.quantity * self.price_per_unit

    def reduce_quantity(self, order_quantity):
        # Reduce crop quantity when an order is placed.
        # Mark crop as 'Out of Stock' if quantity becomes zero.
        
        if self.quantity >= order_quantity:
            self.quantity -= order_quantity
            if self.quantity == 0:
                print(f"{self.crop_name} is now Out of Stock.")  # Debugging
            self.save()
        else:
            raise ValueError(f"Insufficient quantity for {self.crop_name}. Only {self.quantity} {self.unit} available.")



    # # Validation to ensure that price and quantity are positive numbers
    # def clean(self):
    #     if self.quantity <= 0:
    #         raise ValidationError('Quantity must be greater than 0.')
    #     if self.price_per_unit <= 0:
    #         raise ValidationError('Price per unit must be greater than 0.')

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(default="")
    address= models.CharField(max_length=255,blank=True, null=True)
    old_cart= models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.postal_code}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # Active field to indicate cart status

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        # Calculate the total price of all CartItems in the Cart
        return sum(item.total_price() for item in self.cart_items.select_related('crop'))

    def total_items(self):
        # Calculate the total quantity of all items in the Cart
        return sum(item.quantity for item in self.cart_items.all())

    def get_crops(self):
        # Return a list of all crops in the cart
        return [item.crop for item in self.cart_items.all()]

    def deactivate(self):
        # A method to deactivate the cart when the user checks out
        self.active = False
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    crop = models.ForeignKey('Crop', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.crop.crop_name} x {self.quantity}"

    def total_price(self):
        # Calculate the total price for this CartItem (crop price * quantity)
        return self.crop.price_per_unit * self.quantity  # Assuming `price_per_unit` is a field in the `Crop` model
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null= True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100) 
    payment_method = models.CharField(max_length=50, 
                                      choices=[('COD', 'Cash on Delivery'), ('Card', 'Card'), ('UPI', 'UPI')],
                                       default='COD')
    delivery_address = models.TextField(max_length=300)
    status = models.CharField(max_length=50, 
                              default='Pending', 
                              choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ordered_at']

    @property
    def grand_total(self):
        """Calculate grand total including transport fee."""
        return self.total_price + self.transport_fee


    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',null= True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price_per_unit * self.quantity

    def __str__(self):
        return f"{self.crop.crop_name} x {self.quantity}"