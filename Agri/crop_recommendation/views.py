from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
import numpy as np
import pickle as p
from django.contrib.auth.decorators import login_required


#-------------------------------Home---------------------------------

CROP_LABELS = [
    'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
    'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
    'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
    'rice', 'watermelon'
]
@login_required(login_url='login')
def Index(request):
    recent_recommend = crop_recommed.objects.filter().order_by('-cr_id')[:4]

    # Map index values to crop names
    for recommend in recent_recommend:
        try:
            recommend.cr_crop_name = CROP_LABELS[int(recommend.cr_crop)]
        except (ValueError, IndexError):
            recommend.cr_crop_name = "Unknown Crop"

    return render(request, 'index2.html', {'recent_recommend': recent_recommend})

#-------------------------------Crop---------------------------------
@login_required(login_url='login')
def Crop(request):
    crops = crop.objects.all()    
    return render(request,'crop.html',{"crops":crops})

def Crop_details(request,crop_name):  
    crop_details = crop.objects.get(crop_name = crop_name)  
    print(crop_name)  
    return render(request,'crop_details.html',{"crop_details":crop_details})


#-------------------------------Recommendation---------------------------------
# Define the mapping from numeric labels to crop names

@login_required(login_url='login')
def Crop_recommend(request):
    model, accuracy = Recommendation('Crop_Recommendation.pkl')

    if request.method == "POST":
        # Check if the form keys exist
        required_fields = ['farmer_name', 'soil_nitrogen', 'soil_phosphorous', 'soil_potassium', 'soil_ph', 'soil_temperature', 'relative_humidity', 'rainfall']
        
        missing_fields = [field for field in required_fields if not request.POST.get(field)]
        
        if missing_fields:
            error_message = f"Please fill the following fields: {', '.join(missing_fields)}."
            return render(request, 'crop_recommend.html', {'error': error_message, 'accuracy': accuracy})

        result = predict_data(model, request)

        # Convert the predicted crop label to an integer
        try:
            predicted_label = int(result.cr_crop)
            crop_name = CROP_LABELS[predicted_label]
            print("Predicted crop name:", crop_name)
            print("Available crop names in the database:", list(crop.objects.values_list('crop_name', flat=True)))

            # Fetch crop data from the database using the crop name
            result_crop_data = crop.objects.get(crop_name=crop_name)
            print(result_crop_data.crop_image)

            return render(request, 'crop_recommend_view.html', {
                'result': result,
                'predicted_index': predicted_label,
                'crop_name': crop_name,
                'result_crop_data': result_crop_data,
                'CROP_LABELS': CROP_LABELS
            })

        except ValueError:
            return render(request, 'crop_recommend_view.html', {'error': f"Invalid crop prediction value: {result.cr_crop}"})
        except IndexError:
            return render(request, 'crop_recommend_view.html', {'error': f"Invalid crop prediction: {predicted_label}"})
        except crop.DoesNotExist:
            return render(request, 'crop_recommend_view.html', {'error': f"Crop '{crop_name}' not found."})

    return render(request, 'crop_recommend.html', {"accuracy": accuracy})

#-------------------------------About & Contact---------------------------------
def About_us(request):
    return render(request,'about-us.html')

def Contact_us(request):
    return render(request,'contact-us.html')


#-------------------------------Recommendation Model---------------------------------
def Recommendation(recommend_file):    
    pickle_file = open('crop_recommendation/Model/'+recommend_file,'rb')
    model,accuracy = p.load(pickle_file)
    return model,accuracy


#-------------------------------404 Error---------------------------------
def Error_404(request,exception):    
    return render(request,'404.html')


#-------------------------------500 Error---------------------------------
def Error_500(request,exception):    
    return render(request,'500.html')


def predict_data(model,request):                
    farmer_name,soil_nitrogen,soil_phosphorous,soil_potassium = str(request.POST['farmer_name']),int(request.POST['soil_nitrogen']),int(request.POST['soil_phosphorous']),int(request.POST['soil_potassium'])
    soil_temperature,relative_humidity,soil_ph,rainfall = float(request.POST['soil_temperature']),float(request.POST['relative_humidity']),float(request.POST['soil_ph']),float(request.POST['rainfall'])
    try:            
          data = crop_recommed.objects.get(cr_nitrogen=soil_nitrogen,cr_phosphorous=soil_phosphorous,cr_potassium=soil_potassium,cr_ph=soil_ph,cr_temperature=soil_temperature,cr_humidity=relative_humidity,cr_rainfall=rainfall)        

    except crop_recommed.DoesNotExist:    
        predict_details = [soil_nitrogen,soil_phosphorous,soil_potassium,soil_temperature,relative_humidity,soil_ph,rainfall]   
        recommend_crop = model.predict(np.array([predict_details]))            
        data = crop_recommed(cr_farmername=farmer_name,cr_nitrogen=soil_nitrogen,cr_phosphorous=soil_phosphorous,cr_potassium=soil_potassium,cr_ph=soil_ph,cr_temperature=soil_temperature,cr_humidity=relative_humidity,cr_rainfall=rainfall,cr_crop=recommend_crop[0])
        data.save()    
            
    return data


#-------------------------------Admin---------------------------------
# def Admin(request):    
#     return render(request,'agrikol/admin/signin.html')



from django.shortcuts import render
from geopy.geocoders import Nominatim
import requests

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="crop_recommendation")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data['rain'].get('1d', 0) if 'rain' in data else 0
        return temperature, humidity, rainfall
    else:
        return None, None, None


def get_weather_data_view(request):
    weather_data = None
    if request.method == 'POST':
        city_name = request.POST.get('city_name')

        # Fetch the coordinates for the city
        latitude, longitude = get_coordinates(city_name)
        
        if latitude and longitude:
            # Replace with your OpenWeatherMap API Key
            API_KEY = '2f946b6fefbbccd3569c25a7b56ea618'
            temperature, humidity, rainfall = get_weather_data(latitude, longitude, API_KEY)
            
            if temperature is not None:
                weather_data = {
                    'city_name': city_name,
                    'temperature': temperature,
                    'humidity': humidity,
                    'rainfall': rainfall
                }
            else:
                weather_data = {'error': 'Failed to fetch weather data. Please try again.'}
        else:
            weather_data = {'error': 'City not found. Please check the city name.'}

    return render(request, 'crop_recommend.html', {'weather_data': weather_data})


#############################  WEATHER FORECAST AND PAST WITH MAP  ###################
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta

# Replace with your OpenWeatherMap API key
API_KEY_OPENWEATHER = '2f946b6fefbbccd3569c25a7b56ea618'

def fetch_forecast_and_history(lat, lon):
    # Fetch 15-day forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=15&appid={API_KEY_OPENWEATHER}&units=metric"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

    # Fetch historical data for the last 7 days
    historical_data = []
    for days_ago in range(1, 8):
        date = datetime.now() - timedelta(days=days_ago)
        timestamp = int(date.timestamp())
        history_url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={API_KEY_OPENWEATHER}&units=metric"
        history_response = requests.get(history_url)
        if history_response.status_code == 200:
            historical_data.append(history_response.json())

    return forecast_data, historical_data

def get_mapweather_data_view(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        forecast, history = fetch_forecast_and_history(lat, lon)
        if forecast and history:
            return JsonResponse({
                'success': True,
                'forecast': forecast['list'],  # 15-day forecast
                'history': [
                    {
                        'date': datetime.fromtimestamp(day['current']['dt']).strftime('%Y-%m-%d'),
                        'temperature': day['current']['temp'],
                        'humidity': day['current']['humidity']
                    }
                    for day in history
                ],
            })
    return JsonResponse({'success': False, 'error': 'Failed to fetch weather data.'})

from django.shortcuts import render

def map_weather(request):
    # You can pass any additional context as required
    return render(request, 'map_weather.html')  # Ensure the template name matches
