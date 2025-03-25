import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

API_KEY = "3c4fa0d30338ec04088f30af6fb80862"
API_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_KEY + "&units=metric"

def weather_home(request):
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(API_URL.format(city.name)).json()
        if response.get("cod") != 200:
            continue

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    return render(request, 'weather/weather.html', {'weather_data': weather_data, 'form': CityForm()})

def add_city(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    return weather_home(request)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import City
from .serializers import CitySerializer

@api_view(['GET'])
def get_cities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_city_api(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
