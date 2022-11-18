import json
import requests
from .models import City
from .forms import CityForm
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import *


...

@api_view(['GET', 'POST'])
def city_list(request):
    """
 List  customers, or create a new customer.
 """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        cities = City.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(cities, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = CitySerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()
        
        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/cities/?page=' + str(nextPage), 'prevlink': '/api/cities/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

...
@api_view(['GET', 'PUT', 'DELETE'])
def cities_detail(request, pk):
    """
    Retrieve, update or delete a customer by id/pk.
    """
    try:
        city = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CitySerializer(city,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CitySerializer(city, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def environment_data(request):
    from datetime import timezone
    import datetime
    
    dt = datetime.datetime(2021, 1, 1, 0, 0, 0, 0) 
    start_dt = int(dt.replace(tzinfo=timezone.utc).timestamp())

    dt = datetime.datetime(2021, 1, 2, 0, 0, 0, 0) 
    end_dt = int(dt.replace(tzinfo=timezone.utc).timestamp())
    
    city = "London"
    with open('api.properties') as f:
        api_details = f.read()
    api_details=json.loads(api_details,strict=False)    
    url_lat_long = 'http://api.openweathermap.org/geo/1.0/direct?q='+city+'&limit=1&appid='+ api_details['api_key']
    lat_long_data = requests.get(url_lat_long).json()
    long = lat_long_data[0]['lon']
    lat = lat_long_data[0]['lat']
    url_pollution = 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat='+str(lat)+'&lon='+str(long)+'&start='+str(start_dt)+'&end='+str(end_dt)+'&appid='+ api_details['api_key']
    pollution_data = requests.get(url_pollution).json()
    print(pollution_data)
    pollution = pollution_data['list']
    for components in pollution:
        print(components['components'])
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+ api_details['api_key']
    return JsonResponse({'data':'data'})

# Create your views here.
def index(request):
    with open('api.properties') as f:
        api_details = f.read()
    api_details=json.loads(api_details,strict=False)
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+ api_details['api_key']
    cities = City.objects.all()
    weather_data = []
    form = CityForm()
    if request.method == 'POST':
        print(request.POST)
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data' : weather_data,'form':form}
    return render(request,'Farms/index.html',context)
    # return JsonResponse("home",safe=False)