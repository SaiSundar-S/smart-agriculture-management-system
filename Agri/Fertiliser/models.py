from django.db import models

class Fertilizer(models.Model):
    APPLICATION_CHOICES = [
        ('Soil', 'Soil Application'),
        ('Water', 'Water Application'),
    ]
    
    name = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)  # Cost in textual format
    average_cost = models.FloatField()  # Average numerical cost
    quantity = models.CharField(max_length=50)  # Quantity description (e.g., "50 kg bag")
    application_type = models.CharField(max_length=10, choices=APPLICATION_CHOICES)
    image = models.ImageField(upload_to='fertilizer_images/', blank=True, null=True)  # Image field
   
    def __str__(self):
        return self.name

from django.db import models

class FertilizerDetails(models.Model):
    STAGE_CHOICES = [
        ('Pre-Planting', 'Pre-Planting'),
        ('Seedling', 'Seedling Stage'),
        ('Vegetative', 'Vegetative Stage'),
        ('Flowering', 'Flowering Stage'),
        ('Fruiting', 'Fruiting Stage'),
        ('Harvesting', 'Harvesting Stage'),
    ]

    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE, related_name='details')
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    usage_description = models.TextField()  # Details about usage
    recommended_quantity = models.CharField(max_length=50)  # Recommended quantity per stage
    additional_tips = models.TextField(blank=True, null=True)  # Optional tips

    def __str__(self):
        return f"{self.fertilizer.name} - {self.stage}"
