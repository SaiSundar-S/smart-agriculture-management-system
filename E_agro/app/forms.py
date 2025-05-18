from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Farmer, Customer, Crop, ALLUserProfile, Address
from django.core.exceptions import ValidationError
import re


class FarmerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    farm_name= forms.CharField(max_length=200)
    farm_location = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?\d{10,15}$', phone_number):  # Regex for phone numbers
            raise ValidationError("Invalid phone number format.")
        return phone_number

class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    address = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email','address')



class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name','crop_image', 'description', 'category', 'quantity', 'unit', 'price_per_unit', 'location', 'transport_available']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone_number', 'address']
        
# User Profile form (for name and email)
class ALLUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

# Farmer Profile form (for phone number and farm location)
class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'farm_location']

# Customer Profile form (for address and phone number)
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number','address']



class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea, label="Delivery Address")
    payment_method = forms.ChoiceField(choices=[('COD', 'Cash on Delivery'), ('Card', 'Credit/Debit Card'), ('UPI', 'UPI')], label="Payment Method")