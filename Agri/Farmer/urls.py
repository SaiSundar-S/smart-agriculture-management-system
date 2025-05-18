
from .views import *
from django.urls import path,include
from .import views
app_name='Farmer'
urlpatterns = [
    # path('home',views.home,name='home'),
    path('',views.index,name='index'),
    path('header',views.header,name='header'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),


 ]
