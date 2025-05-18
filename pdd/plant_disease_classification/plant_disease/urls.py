from django.urls import path
from . import views
app_name="plant_disease"
urlpatterns = [
    path('index', views.index, name='index'),             # Home page
    path('predict/', views.predict_disease, name='predict_disease'),  # Prediction route
]
