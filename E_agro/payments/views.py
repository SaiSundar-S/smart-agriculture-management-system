from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Customer
from app.forms import CustomerForm
from cart.cart import Cart
from payments.forms import PaymentForm


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        quantities = cart.get_quantities
        cart_products = cart.get_crops
        totals = cart.get_total_price

        if request.user.is_authenticated:

            billing_form = PaymentForm()
            return render(request,'payment/billing_info.html',
                          {
                             'quantities': quantities,
                             'totals': totals,
                             'cart_products': cart_products,
                             'billing_form': billing_form,
                            
                          })
        
        else:
            billing_form = PaymentForm()
            return render(request,'payment/billing_info.html',
                           {
                             'quantities': quantities,
                             'totals': totals,
                             'cart_products': cart_products,
                             'billing_form': billing_form
                              
                            
                          })
        


def payment_success(request):

    return render(request,'payment_success.html',{})
