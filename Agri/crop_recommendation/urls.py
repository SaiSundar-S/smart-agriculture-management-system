from django.urls import path
from .views import *

Error_404 = 'CropRecommendationApp.views.Error_404'
Error_500 = 'CropRecommendationApp.views.Error_500'
app_name = 'crop_recommendation'
urlpatterns = [    
    path('',Index,name='Index'),

    path('Crop/',Crop,name='crop'),
    path('Crop/<str:crop_name>/',Crop_details),    

    path('Recommend/',Crop_recommend,name='crop_recommend'),    
    path('get_weather/', get_weather_data_view, name='get_weather_data_view'),
    path('get_weather_data/', get_mapweather_data_view, name='get_weather_data'),
     path('map-weather/', map_weather, name='map_weather'),
    path('About-Us/',About_us,name='about_us'),
    path('Contact-Us/',Contact_us,name='contact_us'),        
]
