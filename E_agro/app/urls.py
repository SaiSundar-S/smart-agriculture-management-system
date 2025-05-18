from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
app_name='e_agro'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/farmer/', views.register_farmer, name='register_farmer'),
    path('register/customer/', views.register_customer, name='register_customer'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # path('profile/', views.profile_view, name='profile'),  # Profile page URL
    # path('profile/update/', views.profile_update, name='profile_update'),  # Profile update URL
    path('update_profile/', views.update_profile, name='update_profile'),
    path('view_profile/', views.view_profile, name='view_profile'),

    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('add-crop/', views.add_crop, name='add_crop'),
    path('edit-crop/<int:crop_id>/', views.edit_crop, name='edit_crop'),
    path('delete-crop/<int:crop_id>/', views.delete_crop, name='delete_crop'),

    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('crop/<int:crop_id>/', views.crop_detail, name='crop_detail'),  # Crop detail page
    #  path('checkout/', views.checkout, name='checkout'),
    # path('place_order/<int:crop_id>/', views.place_order, name='place_order'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # path('api/addresses/', views.get_addresses, name='get_addresses'),
    # path('api/addresses/add_or_update/', views.add_or_update_address, name='add_or_update_address'),

   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)