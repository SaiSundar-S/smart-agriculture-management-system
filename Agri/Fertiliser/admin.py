from django.contrib import admin
from .models import Fertilizer, FertilizerDetails
# Register your models here.

admin.site.register(Fertilizer)

class FertilizerDetailsInline(admin.TabularInline):
    model = FertilizerDetails
    extra = 1  # Allows adding one new detail inline


class FertilizerAdmin(admin.ModelAdmin):
    inlines = [FertilizerDetailsInline]

admin.site.register(FertilizerDetails)