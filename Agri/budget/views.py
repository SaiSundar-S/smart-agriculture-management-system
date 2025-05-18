from django.shortcuts import render,redirect
from django.http import request
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Crop, SubCrop
from .forms import PredictCostForm

# CMBE/predictcost/views.py
# from .views import APIView
# from .response import Response
# from .models import YourModel
# from .serializers import YourModelSerializer

# class YourEndpointView(APIView):
#     def get(self, request, format=None):
#         items = YourModel.objects.all()
#         serializer = YourModelSerializer(items, many=True)
#         return Response(serializer.data)



# Create your views here.
def home(request):
    return render(request,'home.html')
def fertilizer_recommendation(request):
    return render(request,'home.html')
def disease_prediction(request):
    return render(request,'home.html')
def crop_recommend_view(request):
    return render(request,'home.html')
def budget_estimation(request):
    return render(request,'crop_budget.html')

def select_crop_type(request):
    crops = Crop.objects.all()
    subcrops = SubCrop.objects.none()
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        subcrop_id = request.POST.get('subcrop')
        return redirect('calculator', subcrop_id=subcrop_id)
    
    return render(request, 'select_crop_type.html', {'crops': crops, 'subcrops': subcrops})

def predict_cost(request, subcrop_id):
    subcrop = get_object_or_404(SubCrop, id=subcrop_id)
    if request.method == 'POST':
        form = PredictCostForm(request.POST)
        if form.is_valid():
            predict_cost_instance = form.save(commit=False)
            predict_cost_instance.subcrop = subcrop
            predict_cost_instance.crop = subcrop.crop
            predict_cost_instance.save()
            total_cost = predict_cost_instance.calculate_total_cost()
            
            return render(request, 'result.html', {'total_cost': total_cost})
       
    else:
        form = PredictCostForm()
    return render(request, 'predict_cost.html', {'form': form, 'subcrop': subcrop})


def get_subcrops(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    subcrops = SubCrop.objects.filter(crop=crop).values('id', 'name')
    return JsonResponse({'subcrops': list(subcrops)})


from .forms import PlowingCalculatorForm

def calculator_view(request,subcrop_id):
    subcrop = get_object_or_404(SubCrop, id=subcrop_id)
    result = None
    if request.method == 'POST':
        form = PlowingCalculatorForm(request.POST)
        if form.is_valid():
            hours1 = form.cleaned_data['hours_level1']
            cost1 = form.cleaned_data['cost_per_hour_level1']
            hours2 = form.cleaned_data['hours_level2']
            cost2 = form.cleaned_data['cost_per_hour_level2']
            hours3 = form.cleaned_data['hours_level3']
            cost3 = form.cleaned_data['cost_per_hour_level3']
            
            total1 = hours1 * cost1 if hours1 and cost1 else 0
            total2 = hours2 * cost2 if hours2 and cost2 else 0
            total3 = hours3 * cost3 if hours3 and cost3 else 0
            
            result = total1 + total2 + total3
            request.session['plowing_cost'] = result  # Ensure correct value is set in the session

            return redirect('drip_cost')
    else:
        form = PlowingCalculatorForm()
    
    return render(request, 'calculator.html', {'form': form, 'result': result,'subcrop_id': subcrop_id})


from django.shortcuts import render
from .forms import IrrigationForm
from decimal import Decimal

# Average cost per acre in INR as Decimal
COST_PER_ACRE = {
    'drip': Decimal('60000'),       # average of 50,000 to 70,000
    'sprinkler': Decimal('30000'),  # average of 25,000 to 35,000
    'microjet': Decimal('45000'),   # average of 40,000 to 50,000
}

SUBSIDY_PERCENTAGE = Decimal('0.50')  # 50% subsidy

def drip_cost(request):
    cost = None
    final_cost = None
    if request.method == 'POST':
        form = IrrigationForm(request.POST)
        if form.is_valid():
            irrigation_type = form.cleaned_data['irrigation_type']
            land_area = form.cleaned_data['land_area']
            subsidy = form.cleaned_data['subsidy']
            cost = COST_PER_ACRE[irrigation_type] * land_area
            if subsidy:
                final_cost = cost * (1 - SUBSIDY_PERCENTAGE)
            else:
                final_cost = cost
            request.session['drip_cost'] = str(final_cost) # Save the final cost to the session

            # Render the page again to show the calculated cost
            return render(request, 'drip_cost.html', {'form': form, 'cost': final_cost})

    else:
        form = IrrigationForm()

    return render(request, 'drip_cost.html', {'form': form, 'cost': final_cost})


from django.http import JsonResponse
from .forms import CostEstimationForm

from django.http import JsonResponse
from .forms import CostEstimationForm

def cost_estimation_view(request):
    if request.method == 'POST':
        form = CostEstimationForm(request.POST)
        if form.is_valid():
            estimation = form.save(commit=False)
            total_cost = estimation.calculate_total_cost()
            request.session['cost_estimation_view'] = str(total_cost)
            return JsonResponse({'total_cost': total_cost})
        return redirect('/planting_type')
    else:
        form = CostEstimationForm()

    return render(request, 'mulching.html', {'form': form})

from .forms import CropCostEstimationForm

def estimate_cost(request):
    estimated_cost = None
    if request.method == 'POST':
        form = CropCostEstimationForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method']
            number_of_acres = form.cleaned_data['number_of_acres']
            
            if method == 'planting':
                number_of_plants = form.cleaned_data['number_of_plants']
                cost_per_plant = form.cleaned_data['cost_per_plant']
                estimated_cost = number_of_plants * cost_per_plant * number_of_acres
            
            elif method == 'sowing' or method == 'no_till':
                total_kgs = form.cleaned_data['total_kgs']
                cost_per_kg = form.cleaned_data['cost_per_kg']
                estimated_cost = total_kgs * cost_per_kg * number_of_acres
            request.session['crop_estimation_cost'] = estimated_cost
           
    else:
        form = CropCostEstimationForm()

    return render(request, 'planting_type.html', {'form': form, 'estimated_cost': estimated_cost})

from django.shortcuts import render
from .forms import LabourRateForm, LabourInputForm

def labour(request):
    rate_form = LabourRateForm()
    input_form = LabourInputForm()
    stage_costs = []
    total_cost = 0

    if request.method == 'POST':
        rate_form = LabourRateForm(request.POST)
        input_form = LabourInputForm(request.POST)
        if rate_form.is_valid() and input_form.is_valid():
            male_rate = rate_form.cleaned_data['male_rate']
            female_rate = rate_form.cleaned_data['female_rate']
            
            stages = [
                ('land_preparation', 'Land Preparation'),
                ('planting', 'Planting'),
                ('fertilization', 'Fertilization'),
                ('pest_management', 'Pest Management')
            ]
            
            optional_stages = []
            if input_form.cleaned_data.get('enable_staking'):
                optional_stages.append(('staking', 'Staking'))
            if input_form.cleaned_data.get('enable_weed_removal'):
                optional_stages.append(('weed_removal', 'Weed Removal'))
            
            total_cost = 0
            stage_costs = []
            for stage, stage_name in stages + optional_stages:
                male_count = input_form.cleaned_data.get(f'{stage}_male', 0)
                female_count = input_form.cleaned_data.get(f'{stage}_female', 0)
                if male_count is not None and female_count is not None:
                    cost = (male_count * male_rate) + (female_count * female_rate)
                    stage_costs.append((stage_name, cost))
                    total_cost += cost
            request.session['labour_cost'] = str(total_cost)

    return render(request, 'labour.html', {
        'rate_form': rate_form,
        'input_form': input_form,
        'stage_costs': stage_costs,
        'total_cost': total_cost
    })

# views.py

from django.shortcuts import render
from .forms import HarvestingForm

def harvesting_cost(request):
    total_cost = None
    stage_costs = []
    number_of_harvests = 1

    if request.method == 'POST':
        form = HarvestingForm(request.POST)
        number_of_harvests = int(request.POST.get('number_of_harvests', 1))
        form.add_harvest_fields(number_of_harvests)

        if form.is_valid():
            male_rate = form.cleaned_data['male_rate']
            female_rate = form.cleaned_data['female_rate']
            total_cost = 0

            for i in range(1, number_of_harvests + 1):
                male_labour = form.cleaned_data.get(f'harvest_{i}_male', 0)
                female_labour = form.cleaned_data.get(f'harvest_{i}_female', 0)
                cost = (male_labour * male_rate) + (female_labour * female_rate)
                stage_costs.append((f'Harvest {i}', cost))
                total_cost += cost
            request.session['harvesting_cost'] = total_cost
    else:
        form = HarvestingForm()
        form.add_harvest_fields(number_of_harvests)

    context = {
        'form': form,
        'stage_costs': stage_costs,
        'total_cost': total_cost,
        'number_of_harvests': number_of_harvests,
        'harvest_range': range(1, number_of_harvests + 1)
    }

    return render(request, 'harvesting.html', context)


# estimation/views.py
from django.shortcuts import render
from .forms import CropBudgetForm

def other_budget(request):
    total_cost = None
    if request.method == 'POST':
        form = CropBudgetForm(request.POST)
        if form.is_valid():
            total_sticks = form.cleaned_data.get('total_sticks') or 0
            cost_per_stick = form.cleaned_data.get('cost_per_stick') or 0
            total_kgs_tie1 = form.cleaned_data.get('total_kgs_tie1') or 0
            cost_per_kg_tie1 = form.cleaned_data.get('cost_per_kg_tie1') or 0
            total_kgs_tie2 = form.cleaned_data.get('total_kgs_tie2') or 0
            cost_per_kg_tie2 = form.cleaned_data.get('cost_per_kg_tie2') or 0

            cost_sticks = total_sticks * cost_per_stick
            cost_tie1 = total_kgs_tie1 * cost_per_kg_tie1
            cost_tie2 = total_kgs_tie2 * cost_per_kg_tie2

            total_cost = cost_sticks + cost_tie1 + cost_tie2
            request.session['other_budget_cost'] = str(total_cost)

    else:
        form = CropBudgetForm()

    return render(request, 'other.html', {'form': form, 'total_cost': total_cost})


from .forms import SprayForm

def estimate_sprays(request):
    total_sprays = None
    if request.method == 'POST':
        form = SprayForm(request.POST)
        if form.is_valid():
            crop_name = form.cleaned_data['crop_name']
            growing_period = form.cleaned_data['growing_period']
            spray_interval = form.cleaned_data['spray_interval']

            total_sprays = growing_period // spray_interval

    else:
        form = SprayForm

    return render(request, 'chemicalspray.html', {'form': form, 'total_sprays': total_sprays})




def sidebar_view(request):
    return render(request,'sidebar.html')








from django.shortcuts import render, redirect, get_object_or_404
from .models import Spray, Chemical, SprayChemical
from .forms import SprayForm

def chemicals(request):
    if request.method == 'POST':
        form = SprayForm(request.POST)
        if form.is_valid():
            number_of_sprays = form.cleaned_data['number_of_sprays']
            sprays = [Spray.objects.create(spray_number=i+1) for i in range(number_of_sprays)]
            return redirect('list_sprays')
    else:
        form = SprayForm()
    return render(request, 'chemicals.html', {'form': form})


from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Spray, Chemical, SprayChemical
from decimal import Decimal

def list_sprays(request):
    sprays = Spray.objects.all()
    return render(request, 'list_sprays.html', {'sprays': sprays})

def select_chemicals(request, spray_id):
    spray = get_object_or_404(Spray, id=spray_id)
    spray_type = request.POST.get('spray_type') or request.GET.get('spray_type')
    
    if spray_type:
        chemicals = Chemical.objects.filter(type=spray_type)
    else:
        chemicals = Chemical.objects.none()
    
    selected_chemicals = SprayChemical.objects.filter(spray=spray).select_related('chemical')
    total_cost = sum(sc.chemical.cost for sc in selected_chemicals)
    
    if request.method == 'POST' and 'chemicals' in request.POST:
        selected_chemical_ids = request.POST.get('chemicals')
        selected_chemical_ids_list = selected_chemical_ids.split(',')
        
        # Clear existing SprayChemical entries for the spray
        SprayChemical.objects.filter(spray=spray).delete()
        
        for chemical_id in selected_chemical_ids_list:
            chemical = get_object_or_404(Chemical, id=int(chemical_id))
            SprayChemical.objects.create(spray=spray, chemical=chemical)
        
        # Calculate new total cost
        selected_chemicals = SprayChemical.objects.filter(spray=spray).select_related('chemical')
        total_cost = sum(sc.chemical.cost for sc in selected_chemicals)
        
        # Prepare selected chemicals data for the next view
        selected_chemicals_data = [
            {'name': sc.chemical.name, 'cost': float(sc.chemical.cost)} for sc in selected_chemicals  # Convert Decimal to float
        ]
        
        # Store data in session
        request.session['selected_chemicals'] = selected_chemicals_data
        request.session['total_cost'] = float(total_cost)  # Convert Decimal to float
        
        # Redirect to the total cost page
        return redirect('chemicalcost')
    
    return render(request, 'select_chemicals.html', {
        'spray': spray,
        'chemicals': chemicals,
        'selected_chemicals': selected_chemicals,
        'spray_type': spray_type,
        'total_cost': total_cost,
    })
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Allow AJAX requests without CSRF token
def delete_spray(request, spray_id):
    if request.method == 'DELETE':
        try:
            spray = Spray.objects.get(id=spray_id)
            spray.delete()  # Delete the spray
            return JsonResponse({'message': 'Spray removed successfully!'}, status=200)
        except Spray.DoesNotExist:
            return JsonResponse({'error': 'Spray not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def chemicalcost(request):
    selected_chemicals = request.session.get('selected_chemicals', [])
    total_cost = request.session.get('total_cost', 0.0)
    request.session['spray_cost'] = total_cost
    
    return render(request, 'chemicalcost.html', {
        'selected_chemicals': selected_chemicals,
        'total_cost': total_cost,
        
    })


def calculate_total_cost(request):
    # Retrieve costs from session or default to 0
    total_costs = {
        'plowing_cost': float(request.session.get('plowing_cost', 0)),
        'drip_cost': float(request.session.get('drip_cost', 0)),
        'labour_cost': float(request.session.get('labour_cost', 0)),
        'harvesting_cost': float(request.session.get('harvesting_cost', 0)),
        'other_budget_cost': float(request.session.get('other_budget_cost', 0)),
        'spray_cost': float(request.session.get('spray_cost', 0)),
        'fertilizer_cost': float(request.session.get('fertilizer_cost', 0)),
    }

    # Calculate total cost
    total_cost = sum(total_costs.values())

    # Retrieve crop name from session (or provide a default)
    crop_name = request.session.get('crop_name', 'Unknown Crop')

    # Debugging session data
    print(f"Session Data: {request.session.items()}")

    # Render the billing template
    return render(request, 'billing.html', {
        'total_costs': total_costs,
        'total_cost': total_cost,
        'crop_name': crop_name,  # Pass crop name to the template
    })




from django.shortcuts import render, redirect
from .models import Fertilizer, SelectedFertilizer
from .forms import FertilizerTypeForm

def select_fertilizer_type(request):
    if request.method == 'POST':
        form = FertilizerTypeForm(request.POST)
        if form.is_valid():
            selected_type = form.cleaned_data['fertilizer_type']
            return redirect('select_fertilizers', fertilizer_type=selected_type)
    else:
        form = FertilizerTypeForm()
    return render(request, 'select_fertilizer_type.html', {'form': form})

def select_fertilizers(request, fertilizer_type):
    # Fetch fertilizers matching the application type
    fertilizers = Fertilizer.objects.filter(application_type=fertilizer_type)
    
    if request.method == 'POST':
        selected_fertilizers_ids = request.POST.get('selected_fertilizers', '').split(',')
        total_cost = float(request.POST.get('total_cost', '0') or '0')  # Default to 0 if empty

        selected_fertilizers_data = []

        for fert_id in selected_fertilizers_ids:
            if fert_id:  # Ensure fert_id is not empty
                fertilizer = Fertilizer.objects.get(id=fert_id)
                selected_fertilizers_data.append({
                    'name': fertilizer.name,
                    'cost': float(fertilizer.cost),
                    'image': fertilizer.image.url if fertilizer.image else None
                })

        # Save selected fertilizers and total cost to the session
        request.session['selected_fertilizers'] = selected_fertilizers_data
        request.session['fertilizer_cost'] = total_cost

        return redirect('fertilizer_cost')
    
    return render(request, 'select_fertilizers.html', {'fertilizers': fertilizers})



def fertilizer_cost(request):
    selected_fertilizers = request.session.get('selected_fertilizers', [])
    total_cost = request.session.get('fertilizer_cost', 0)
    request.session['fertilizer_cost'] = total_cost
    return render(request, 'fertilisercost.html', {
        'selected_fertilizers': selected_fertilizers,
        'total_cost': total_cost
    })
#################################################################################################
from django.shortcuts import render, redirect
from .models import Crop, SubCrop

def overallcost(request):
     # Fetch subcrops based on selected crop
    
    return render(request, 'staticpage.html', {'crops': crops, 'subcrops': subcrops})
# views.py

# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import PlowingCalculatorForm
# from .models import SubCrop

# def calculator_view(request, subcrop_id):
#     # Fetch the subcrop by ID
#     subcrop = get_object_or_404(SubCrop, id=subcrop_id)
#     result = None
    
#     if request.method == 'POST':
#         # Process the form data
#         form = PlowingCalculatorForm(request.POST)
#         if form.is_valid():
#             hours1 = form.cleaned_data['hours_level1']
#             cost1 = form.cleaned_data['cost_per_hour_level1']
#             hours2 = form.cleaned_data['hours_level2']
#             cost2 = form.cleaned_data['cost_per_hour_level2']
#             hours3 = form.cleaned_data['hours_level3']
#             cost3 = form.cleaned_data['cost_per_hour_level3']
            
#             # Calculate the total cost for each level
#             total1 = hours1 * cost1 if hours1 and cost1 else 0
#             total2 = hours2 * cost2 if hours2 and cost2 else 0
#             total3 = hours3 * cost3 if hours3 and cost3 else 0
            
#             # Sum the total costs
#             result = total1 + total2 + total3
            
#             # Store the result in session to use later in the card
#             request.session['plowing_cost'] = result

#             # Redirect to staticpage to show the updated cost
#             return redirect('staticpage')  # Redirect to the static page

#     else:
#         # Initial form load
#         form = PlowingCalculatorForm()

#     # Render the form and pass the subcrop, result, and form to the template
#     return render(request, 'calculator.html', {
#         'form': form,
#         'subcrop_id': subcrop_id,
#         'subcrop': subcrop
#     })

def header(request):
    return render(request, 'header.html')
