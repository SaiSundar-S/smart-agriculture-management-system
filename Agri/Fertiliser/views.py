from django.shortcuts import render
from .models import Fertilizer

from django.shortcuts import render
from django.http import HttpResponse
import pickle

# Create your views here.
def ferti_home(request):
    return render(request,'fertihome.html')

def fertilizers_list(request):
    fertilizers=Fertilizer.objects.all()
    return render(request,'fertilizers.html',{'fertilizers':fertilizers})



# Load models
model = pickle.load(open("E:/SAMS/Agri/Fertiliser/Model/classifier.pkl", "rb"))
ferti = pickle.load(open("E:/SAMS/Agri/Fertiliser/Model/fertilizer.pkl", "rb"))

# def home(request):
#     return render(request, "plantindex.html")

def model1(request):
    if request.method == "POST":
        temp = request.POST.get("temp")
        humi = request.POST.get("humid")
        mois = request.POST.get("mois")
        soil = request.POST.get("soil")
        crop = request.POST.get("crop")
        nitro = request.POST.get("nitro")
        pota = request.POST.get("pota")
        phosp = request.POST.get("phos")
        
        # Validate input
        if not all([temp, humi, mois, soil, crop, nitro, pota, phosp]):
            return render(request, "Model1.html", {"x": "Please fill in all fields."})
        
        try:
            input_data = list(map(int, [temp, humi, mois, soil, crop, nitro, pota, phosp]))
            prediction = ferti.classes_[model.predict([input_data])]
            return render(request, "Model1.html", {"x": prediction})
        except ValueError:
            return render(request, "Model1.html", {"x": "Invalid input. Please enter numeric values."})
    
    return render(request, "Model1.html")

def detail(request):
    return render(request, "Detail.html")


# ##########chatgpt############
# from django.shortcuts import render
# from .utils import load_fertilizer_model, preprocess_input

# def predict_fertilizer(request):
#     if request.method == 'POST':
#         try:
#             # Retrieve form inputs
#             temp = float(request.POST.get("temp"))
#             humi = float(request.POST.get("humi"))
#             mois = float(request.POST.get("mois"))
#             soil = request.POST.get("soil")
#             crop = request.POST.get("crop")
#             nitro = float(request.POST.get("nitro"))
#             pota = float(request.POST.get("pota"))
#             phosp = float(request.POST.get("phosp"))
            
#             # Prepare input data
#             input_data = [temp, humi, mois, soil, crop, nitro, pota, phosp]

#             # Load the model
#             model = load_fertilizer_model()

#             # Preprocess input (encoding categorical variables)
#             processed_input = preprocess_input(input_data)

#             # Make prediction
#             prediction = model.predict([processed_input])[0]

#             # Render the result
#             return render(request, 'result.html', {'prediction': prediction})
#         except Exception as e:
#             # Handle errors gracefully
#             return render(request, 'predict.html', {'error': str(e)})
#     return render(request, 'predict.html')

from django.shortcuts import render, get_object_or_404
from .models import Fertilizer, FertilizerDetails

def fertilizer_detail(request, fertilizer_name,):
    fertilizer = get_object_or_404(Fertilizer, name=fertilizer_name)
    fertilizers=Fertilizer.objects.all()
    # Convert QuerySet to a list of dictionaries
    info = FertilizerDetails.objects.filter(fertilizer=fertilizer)
    details = list(fertilizer.details.values('stage', 'usage_description', 'recommended_quantity'))
    
    return render(request, 'fertilizer_detail.html', {
        'fertilizers':fertilizers,
        'fertilizer': fertilizer,
        'details': details, 
        'info':info,
          # Pass the list to the template
    })
