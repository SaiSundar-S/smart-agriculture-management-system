from django.urls import path
from .import views
app_name='Fertiliser'
urlpatterns=[
    path('',views.ferti_home,name='ferti_home'),
    path('fertilizer/',views.fertilizers_list,name="fertilizers_list"),
    #  path("home/", views.home, name="home"),
    path("model1/", views.model1, name="model1"),
    path("detail/", views.detail, name="detail"),
    # path('predict/', views.predict_fertilizer, name='predict_fertilizer'),
     path('fertilizer/<str:fertilizer_name>/', views.fertilizer_detail, name='fertilizer_detail'),
]