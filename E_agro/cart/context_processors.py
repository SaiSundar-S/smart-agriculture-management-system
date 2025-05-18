from .cart import Cart

# create context processor so our cart works on all pages
def cart_context(request):
    return {'cart': Cart(request)} 