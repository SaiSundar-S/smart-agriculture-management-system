# budget/models.py

from django.db import models



class Crop(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SubCrop(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class PredictCost(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    subcrop = models.ForeignKey(SubCrop, on_delete=models.CASCADE)
    land_area = models.FloatField()
    cultivation_type = models.CharField(max_length=200)
    fertilizer = models.CharField(max_length=200)
   
    mulching_type = models.CharField(max_length=200)
    plants = models.IntegerField()
    sticks_threads=models.IntegerField()
    labour = models.DecimalField(max_digits=10, decimal_places=2)
    harvesting = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_cost(self):
        total_cost = (
            self.sticks_threads+
            self.labour +
            self.harvesting
        )
        return total_cost

    def __str__(self):
        return f'{self.crop.name} - {self.subcrop.name}'


from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)



class CostEstimation(models.Model):
    needs_mulching = models.BooleanField(default=False)
    area_in_acres = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cost_per_acre = models.DecimalField(max_digits=10, decimal_places=2)  # Example cost per acre

    def calculate_total_cost(self):
        if self.needs_mulching and self.area_in_acres:
            return self.area_in_acres * self.cost_per_acre
        return 0


# sprays/models.py
from django.db import models

class Spray(models.Model):
    spray_number = models.IntegerField()


class Chemical(models.Model):
    TYPE_CHOICES = [
        ('fungicide', 'Fungicide'),
        ('insecticide', 'Insecticide'),
        ('herbicide', 'Herbicide'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=50)  # Adjust max_length as per your data
    def __str__(self):
        return self.name

class SprayChemical(models.Model):
    spray = models.ForeignKey(Spray, on_delete=models.CASCADE)
    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.spray} - {self.chemical} ({self.quantity})"



from django.db import models

class Fertilizer(models.Model):
    name = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)  # Save the original cost string
    avg_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    application_type = models.CharField(max_length=50, choices=[('soil', 'Soil'), ('water', 'Water')], default='soil')
    image = models.ImageField(upload_to='fertilizer_images/', blank=True, null=True)  # Image field


    def __str__(self):
        return self.name


class SelectedFertilizer(models.Model):
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
