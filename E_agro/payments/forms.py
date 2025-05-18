from django import forms

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}),required=True)
    card_number =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}),required=True)
    car_exp_date =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiration Date'}),required=True)
    card_cvv_number =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}),required=True)
    card_address = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address'}),required=True)
    card_city =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing City'}),required=True)
    card_state =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing State'}),required=True)
    card_pincode =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Pipcode'}),required=True)
    card_country =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Country'}),required=True)
