from django.contrib import admin
from .models import Farmer, Customer, Address, Crop, Cart, CartItem, Order, OrderItem

admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Crop)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


