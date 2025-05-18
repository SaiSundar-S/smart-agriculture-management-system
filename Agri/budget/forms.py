# budget/forms.py

from django import forms
from .models import PredictCost

class PredictCostForm(forms.ModelForm):
    class Meta:
        model = PredictCost
        fields = ['land_area', 'cultivation_type', 'fertilizer', 'mulching_type', 'plants', 'sticks_threads', 'labour', 'harvesting']
        labels = {
            
            'land_area': 'Land Area (in acres)',
            'cultivation_type': 'Cultivation Type',
            'fertilizer': 'Fertilizer',
            'mulching_type': 'Mulching Type',
            'plants': 'Number of Plants',
            'sticks_threads': 'Number of Sticks/Threads',
            'labour': 'Labour Cost',
            'harvesting': 'Harvesting Cost'
        }
        widgets = {
            'fertilizer': forms.CheckboxSelectMultiple(choices=[('manure', 'Manure'), ('chemical', 'Chemical')]),
        }

class PlowingCalculatorForm(forms.Form):
    cultivation_type = forms.CharField(label='Cultivation Type')
    hours_level1 = forms.FloatField(label='Hours for Level 1', required=False,initial=0)
    cost_per_hour_level1 = forms.FloatField(label='Cost per Hour for Level 1', required=False,initial=0)
    hours_level2 = forms.FloatField(label='Hours for Level 2', required=False,initial=0)
    cost_per_hour_level2 = forms.FloatField(label='Cost per Hour for Level 2', required=False,initial=0)
    hours_level3 = forms.FloatField(label='Hours for Level 3', required=False,initial=0)
    cost_per_hour_level3 = forms.FloatField(label='Cost per Hour for Level 3', required=False,initial=0)
    total_cost = forms.FloatField(widget=forms.HiddenInput(), required=False,initial=0)





from django import forms

IRRIGATION_CHOICES = [
    ('drip', 'Drip Irrigation'),
    ('sprinkler', 'Sprinkler Irrigation'),
    ('microjet', 'Microjet Irrigation'),
]

class IrrigationForm(forms.Form):
    irrigation_type = forms.ChoiceField(choices=IRRIGATION_CHOICES, widget=forms.HiddenInput)
    land_area = forms.DecimalField(label='Land Area (in acres)', min_value=0.1)
    subsidy = forms.BooleanField(required=False, label='Apply for small farmer subsidy')



from .models import CostEstimation

class CostEstimationForm(forms.ModelForm):
    class Meta:
        model = CostEstimation
        fields = ['needs_mulching', 'area_in_acres', 'cost_per_acre']  # Ensure cost_per_acre is included

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['needs_mulching'].widget.attrs.update({'class': 'form-control'})
        self.fields['area_in_acres'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter area in acres'})
        self.fields['cost_per_acre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter cost per acre'})
        
        # Hide the area_in_acres and cost_per_acre fields initially
        self.fields['area_in_acres'].widget = forms.HiddenInput()
        self.fields['cost_per_acre'].widget = forms.HiddenInput()

from django import forms

class CropCostEstimationForm(forms.Form):
    METHOD_CHOICES = [
        ('sowing', 'Sowing'),
        ('planting', 'Planting'),
        ('no_till', 'No-till Farming'),
    ]
    method = forms.ChoiceField(choices=METHOD_CHOICES, label='Method')
    number_of_acres = forms.FloatField(label='Number of Acres')

    # Fields for planting
    number_of_plants = forms.IntegerField(label='Number of Plants', required=False)
    cost_per_plant = forms.FloatField(label='Cost per Plant', required=False)

    # Fields for sowing and no-till farming
    total_kgs = forms.FloatField(label='Total Number of Kgs', required=False)
    cost_per_kg = forms.FloatField(label='Cost per Kg', required=False)

from django import forms

class LabourRateForm(forms.Form):
    male_rate = forms.DecimalField(label='Male Labour Rate', max_digits=10, decimal_places=2)
    female_rate = forms.DecimalField(label='Female Labour Rate', max_digits=10, decimal_places=2)

class LabourInputForm(forms.Form):
    land_preparation_male = forms.IntegerField(label='Male Labour', min_value=0)
    land_preparation_female = forms.IntegerField(label='Female Labour', min_value=0)
    planting_male = forms.IntegerField(label='Male Labour', min_value=0)
    planting_female = forms.IntegerField(label='Female Labour', min_value=0)
    fertilization_male = forms.IntegerField(label='Male Labour', min_value=0)
    fertilization_female = forms.IntegerField(label='Female Labour', min_value=0)
    pest_management_male = forms.IntegerField(label='Male Labour', min_value=0)
    pest_management_female = forms.IntegerField(label='Female Labour', min_value=0)
    enable_staking = forms.BooleanField(label='Enable Staking', required=False)
    staking_male = forms.IntegerField(label='Male Labour', min_value=0, required=False)
    staking_female = forms.IntegerField(label='Female Labour', min_value=0, required=False)
    enable_weed_removal = forms.BooleanField(label='Enable Weed Removal', required=False)
    weed_removal_male = forms.IntegerField(label='Male Labour', min_value=0, required=False)
    weed_removal_female = forms.IntegerField(label='Female Labour', min_value=0, required=False)
    enable_harvesting = forms.BooleanField(label='Enable Harvesting', required=False)
    number_of_harvests = forms.IntegerField(label='Number of Harvests', min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, 11):  # Assuming a maximum of 10 harvests
            self.fields[f'harvest_{i}_male'] = forms.IntegerField(label=f'Harvest {i} - Male Labour', min_value=0, required=False)
            self.fields[f'harvest_{i}_female'] = forms.IntegerField(label=f'Harvest {i} - Female Labour', min_value=0, required=False)
## forms.py

from django import forms

class HarvestingForm(forms.Form):
    number_of_harvests = forms.IntegerField(label="Number of Harvests", min_value=1)
    male_rate = forms.FloatField(label="Male Labour Rate (₹)")
    female_rate = forms.FloatField(label="Female Labour Rate (₹)")

    def add_harvest_fields(self, number_of_harvests):
        for i in range(1, number_of_harvests + 1):
            self.fields[f'harvest_{i}_male'] = forms.IntegerField(label=f'Harvest {i} - Male Labour', min_value=0, required=False)
            self.fields[f'harvest_{i}_female'] = forms.IntegerField(label=f'Harvest {i} - Female Labour', min_value=0, required=False)

# estimation/forms.py
from django import forms

class CropBudgetForm(forms.Form):
    total_sticks = forms.IntegerField(required=False, label='Total Sticks')
    cost_per_stick = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Cost per Stick')

    total_kgs_tie1 = forms.IntegerField(required=False, label='Total Kgs for Tie 1')
    cost_per_kg_tie1 = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Cost per Kg for Tie 1')

    total_kgs_tie2 = forms.IntegerField(required=False, label='Total Kgs for Tie 2')
    cost_per_kg_tie2 = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Cost per Kg for Tie 2')


from django import forms
from .models import Spray, Chemical

class SprayForm(forms.Form):
    number_of_sprays = forms.IntegerField(min_value=1)

class ChemicalForm(forms.Form):
    chemical_type = forms.ChoiceField(choices=[('', 'Select Type'), ('fungicide', 'Fungicide'), ('insecticide', 'Insecticide'), ('herbicide', 'Herbicide')])

    def __init__(self, *args, **kwargs):
        chemical_type = kwargs.pop('chemical_type')
        super().__init__(*args, **kwargs)
        if chemical_type:
            chemicals_queryset = Chemical.objects.filter(type=chemical_type)
            self.fields['chemicals'] = forms.ModelMultipleChoiceField(queryset=chemicals_queryset, widget=forms.CheckboxSelectMultiple)
            for chemical in chemicals_queryset:
                self.fields[f'quantity_{chemical.id}'] = forms.IntegerField(label=f'{chemical.name} Quantity', min_value=1, initial=1) 


##########fertilizer form #######
# from .models import Fertilizer, UserSelection

# class UserSelectionForm(forms.ModelForm):
#     soil_fertilizers = forms.ModelMultipleChoiceField(
#         queryset=Fertilizer.objects.filter(application_type='soil'),
#         widget=forms.CheckboxSelectMultiple,
#         required=True
#     )
#     water_fertilizers = forms.ModelMultipleChoiceField(
#         queryset=Fertilizer.objects.filter(application_type='water'),
#         widget=forms.CheckboxSelectMultiple,
#         required=True
#     )

#     class Meta:
#         model = UserSelection
#         fields = ['soil_fertilizers', 'water_fertilizers']


from .models import Fertilizer

class FertilizerTypeForm(forms.Form):
    FERTILIZER_TYPES= [
        ('soil', 'Soil Fertilizer'),
        ('water_soluble', 'Water Soluble'),
        ('manure', 'Manure'),
    ]
    fertilizer_type = forms.ChoiceField(choices=FERTILIZER_TYPES, label='Select Fertilizer Type')
class FertilizerSelectionForm(forms.Form):
    fertilizers = forms.ModelMultipleChoiceField(queryset=Fertilizer.objects.all(), widget=forms.CheckboxSelectMultiple)
