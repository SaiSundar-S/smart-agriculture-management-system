"""
URL configuration for Agri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Farmer.urls')),
    # path('marketing/',include('marketing.urls')),
    path('crop_recommendation/',include('crop_recommendation.urls')),
    # path('weather/',include('weather.urls')),
    path('budget/',include('budget.urls')),
    path('Fertiliser/',include('Fertiliser.urls')),
   path('plant_disease/', include('plant_disease.urls')), 
   path('app/',include('app.urls')),
   path('cart/',include('cart.urls')),
   path('payments/',include('payments.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
