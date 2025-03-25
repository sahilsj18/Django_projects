from django.urls import path
from django.urls import path
from .views import weather_home, add_city, get_cities, add_city_api

urlpatterns = [
    path('', weather_home, name='weather_home'),
    path('add_city/', add_city, name='add_city'),
    path('api/cities/', get_cities, name='api_get_cities'),
    path('api/add_city/', add_city_api, name='api_add_city'),
]
