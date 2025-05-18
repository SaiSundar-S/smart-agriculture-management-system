from django.contrib import admin
from django.urls import path
from .import views
from .views import calculator_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('budget_estimation/', views.budget_estimation, name='budget_estimation'),
    path('home',views.home,name='home'),
    path('fertilizer_recommendation/', views.fertilizer_recommendation, name='fertilizer_recommendation'),
    path('disease_prediction/',views.disease_prediction, name='disease_prediction'),
    path('crop_recommend/', views.crop_recommend_view, name='crop_recommend'),
   
    path('select_crop_type/', views.select_crop_type, name='select_crop_type'),
    path('predict/<int:subcrop_id>/', views.predict_cost, name='predict_cost'),
    path('api/subcrops/<int:crop_id>/', views.get_subcrops, name='get_subcrops'),
    path('calculator/<int:subcrop_id>/', views.calculator_view, name='calculator'),
    path('drip_cost/', views.drip_cost, name='drip_cost'),
    path('mulching_cost/', views.cost_estimation_view, name='cost_estimation'),
    path('planting_type', views.estimate_cost, name='estimate_cost'),
    path('labour_cost/',views.labour,name='labour'),
    path('harvesting_cost/', views.harvesting_cost, name='harvesting_cost'),
    path('other/', views.other_budget, name='other_budget'),
    path('chemicals/', views.chemicals, name='chemicals'),
    path('list_sprays/', views.list_sprays, name='list_sprays'),
    path('select_chemicals/<int:spray_id>/', views.select_chemicals, name='select_chemicals'),
     path('delete-spray/<int:spray_id>/', views.delete_spray, name='delete_spray'),
    path('chemicalcost/', views.chemicalcost, name='chemicalcost'),
    

    path('select-fertilizer-type/', views.select_fertilizer_type, name='select_fertilizer_type'),
    path('select-fertilizers/<str:fertilizer_type>/', views.select_fertilizers, name='select_fertilizers'),
    path('fertilizercost/',views.fertilizer_cost,name='fertilizer_cost'),
    path('billing/', views.calculate_total_cost, name='calculate_total_cost'),
    # path('your-endpoint/', views.YourEndpointView.as_view(), name='your-endpoint'),
   path('staticpage/',views.overallcost,name='staticpage'),
  
path('header/',views.header,name='header'),

 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('display_chemicals_cost/<int:spray_id>/', views.display_chemicals_cost, name='display_chemicals_cost'),    
    # path('select/', views.select_fertilizers, name='select_fertilizers'),
    # path('results/<int:selection_id>/', views.results, name='results'),