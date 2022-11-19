import logging
import json
import requests
from datetime import timezone
import datetime
from .models import City, ComponentsData
from .forms import CityForm
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from rest_framework.decorators import api_view
from .serializers import *
logger = logging.getLogger('file')

@api_view(['GET'])
def city_envcomponents(request, city):
    try:
     components = ComponentsData.objects.filter(city=city)
    except Exception as exception:
        logger.error("Exception",exception)
    no_list = []
    so2_list = []
    nh3_list = []
    co_list = []
    for component in components:
        no_list.append(round(component.no))
        co_list.append(round(component.co))
        so2_list.append(round(component.so2))
        nh3_list.append(round(component.nh3))
    return JsonResponse({'no_list': no_list, 'co_list': co_list, 'so2_list': so2_list, 'nh3_list': nh3_list})


def environment_data(request, city):

    dt = datetime.datetime(2021, 1, 1, 0, 0, 0, 0)
    start_dt = int(dt.replace(tzinfo=timezone.utc).timestamp())

    dt = datetime.datetime(2021, 1, 2, 0, 0, 0, 0)
    end_dt = int(dt.replace(tzinfo=timezone.utc).timestamp())

    # city = "Paris"
    with open('api.properties') as f:
        api_details = f.read()
    api_details = json.loads(api_details, strict=False)
    url_lat_long = 'http://api.openweathermap.org/geo/1.0/direct?q=' + \
        city+'&limit=1&appid=' + api_details['api_key']
    lat_long_data = requests.get(url_lat_long).json()
    long = lat_long_data[0]['lon']
    lat = lat_long_data[0]['lat']
    url_pollution = 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=' + \
        str(lat)+'&lon='+str(long)+'&start='+str(start_dt) + \
        '&end='+str(end_dt)+'&appid=' + api_details['api_key']
    pollution_data = requests.get(url_pollution).json()
    print(pollution_data)
    pollution = pollution_data['list']
    model_object_list = []
    model_object_dict = {}
    for components in pollution:
        model_object_dict['city'] = city
        model_object_dict['date'] = components['dt']
        model_object_dict['no'] = components['components']['no']
        model_object_dict['co'] = components['components']['co']
        model_object_dict['so2'] = components['components']['so2']
        model_object_dict['nh3'] = components['components']['nh3']
        print(model_object_dict)

        model_object_list.append(ComponentsData(**model_object_dict))
    try:
     ComponentsData.objects.bulk_create(
        model_object_list, ignore_conflicts=True)
    except Exception as exception:
        logger.error("Exception",exception)
    return JsonResponse({'data': 'data'})


def index(request):
    with open('api.properties') as f:
        api_details = f.read()
    api_details = json.loads(api_details, strict=False)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + \
        api_details['api_key']
    try:    
        cities = City.objects.all()
    except Exception as exception:
        logger.error("Exception",exception)
    weather_data = []
    form = CityForm()
    if request.method == 'POST':
        print(request.POST)
        form = CityForm(request.POST)
        form.save()
        environment_data(HttpRequest, request.POST.get('name'))
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'Farms/index.html', context)
