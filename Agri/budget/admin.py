
from django.contrib import admin

from .models import Crop, SubCrop, PredictCost
from .models import Spray, Chemical, SprayChemical,Fertilizer,SelectedFertilizer

admin.site.register(Crop)
admin.site.register(SubCrop)
admin.site.register(PredictCost)
admin.site.register(Chemical)
admin.site.register(Spray)
admin.site.register(SprayChemical)
admin.site.register(Fertilizer)
admin.site.register(SelectedFertilizer)