from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_update/', views.cart_update, name='cart_update'),
    path('cart_delete/', views.cart_delete, name='cart_delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path("order-confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)