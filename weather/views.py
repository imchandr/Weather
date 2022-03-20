import json
import stat
from urllib import response
import requests
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from weather.forms import CityForm
from weather.models import City
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
import datetime
import calendar

import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def index(request):
    return render(request, 'index.html')

def home_page(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=57b8cef8d3469a4f9f9bc8bed02ea116'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"

    print(err_msg)
    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        print('\n\n r data', r)
        city_weather  = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/city_weather_list.html',context)

def city_weather_details(request, city_name):
    city = get_object_or_404(City, name=city_name)
    
   
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=57b8cef8d3469a4f9f9bc8bed02ea116'
    
    print('\n\n url: \n', url)  
    
    #parse the Json
    req = requests.get(url)
    data = req.json()

    #retriving the name, the longitude and latitude
    name = data['name']
    lon = data['coord']['lon']
    lat = data['coord']['lat']

    
    # One Call Api to get the 8 day forecast and exclude the minutely and hourly
    exclude = "minute,hourly"

    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid=57b8cef8d3469a4f9f9bc8bed02ea116'


    #parsing the JSON
    req2 = requests.get(url2, verify=False)
    data2 = req2.json()
    
    print('\n\n one-call urls data:\n',data2)

    #retriving temp for the day, the night and the weather conditions, and icon
    forcast_date = []
    day_name = []
    days_temp = []
    nights_temp = []
    descr = []
    icon = []
    
    #access 'daily' for retriving api data
    for i in data2['daily']:
            
            #converting Kelvin, to C by -273.15 for every datapoint and the round numbers to 2 digits
            #day temp
            days_temp.append(round(i['temp']['day'] - 273.15,2))
            
            #Nights temp
            nights_temp.append(round(i['temp']['night'] - 273.15,2))
            
            #weather condition and the description from api
            #'weather' [0] 'main' + 'weather' [0] 'description'
            descr.append(i['weather'][0]['main'] + ": " +i['weather'][0]['description'])
            icon.append(i['weather'][0]['icon'])
            forc_date = datetime.datetime.fromtimestamp(int(i["dt"]))
            forcast_date.append(forc_date)
            forcasted_date = datetime.datetime.fromtimestamp(int(i["dt"])).strftime('%Y-%m-%d ')
            day = calendar.day_name[datetime.datetime.strptime(forcasted_date, '%Y-%m-%d ').weekday()]
            day_name.append(day)
    
    weather_data = zip(forcast_date, day_name, days_temp, nights_temp, descr, icon)

   
    context = {
        
        'city':city,
        'data': list(weather_data)
    }
    return render(request,'weather/city_weather_details.html', context )
  

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('/weather')

def city_weather_details_api(request,city_name):
    city = get_object_or_404(City, name = city_name)
   
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=57b8cef8d3469a4f9f9bc8bed02ea116'
    
    print('\n\n url: \n', url)  
    
    #parsing the Json
    req = requests.get(url)
    data = req.json()

    #retriving the name, the longitude and latitude
    name = data['name']
    lon = data['coord']['lon']
    lat = data['coord']['lat']

    print('\n\n name lat, long of location: \n',name, lon, lat)
    
    # One Call Api to retrive forecast wih exclude the minutely and hourly
    exclude = "minute,hourly"

    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid=57b8cef8d3469a4f9f9bc8bed02ea116'
    
    print('\n\n one-call url:\n',url2)

    #parsing the JSON
    req2 = requests.get(url2, verify=False)
    data2 = req2.json()
    

    
    forcasted_date1 = datetime.datetime.fromtimestamp(int(data2['daily'][0]["dt"])).strftime('%Y-%m-%d ')
    day1 = calendar.day_name[datetime.datetime.strptime(forcasted_date1, '%Y-%m-%d ').weekday()]
    
    forcasted_date2 = datetime.datetime.fromtimestamp(int(data2['daily'][1]["dt"])).strftime('%Y-%m-%d ')
    day2 = calendar.day_name[datetime.datetime.strptime(forcasted_date2, '%Y-%m-%d ').weekday()]
    
    forcasted_date3 = datetime.datetime.fromtimestamp(int(data2['daily'][2]["dt"])).strftime('%Y-%m-%d ')
    day3 = calendar.day_name[datetime.datetime.strptime(forcasted_date3, '%Y-%m-%d ').weekday()]
    
    forcasted_date4 = datetime.datetime.fromtimestamp(int(data2['daily'][3]["dt"])).strftime('%Y-%m-%d ')
    day4 = calendar.day_name[datetime.datetime.strptime(forcasted_date4, '%Y-%m-%d ').weekday()]
    
    
    
    weather_forcast = {'day_1':{'date':forcasted_date1,
                                'day':day1,
                                'dt':round(data2['daily'][0]['temp']['day'] - 273.15,2), 
                                'nt':round(data2['daily'][0]['temp']['night'] - 273.15,2),
                                'desc': data2['daily'][0]['weather'][0]['main'] + ": " +data2['daily'][0]['weather'][0]['description'],
                                'icon':data2['daily'][0]['weather'][0]['icon'],},
                       'day_2':{'date':forcasted_date2,
                                'day':day2,
                                'dt':round(data2['daily'][1]['temp']['day'] - 273.15,2), 
                                'nt':round(data2['daily'][1]['temp']['night'] - 273.15,2),
                                'desc': data2['daily'][1]['weather'][0]['main'] + ": " +data2['daily'][0]['weather'][0]['description'],
                                'icon':data2['daily'][1]['weather'][0]['icon'],},
                       'day_3':{'date':forcasted_date3,
                                'day':day3,
                                'dt':round(data2['daily'][2]['temp']['day'] - 273.15,2), 
                                'nt':round(data2['daily'][2]['temp']['night'] - 273.15,2),
                                'desc': data2['daily'][2]['weather'][0]['main'] + ": " +data2['daily'][0]['weather'][0]['description'],
                                'icon':data2['daily'][2]['weather'][0]['icon'],},
                       'day_4':{'date':forcasted_date4,
                                'day':day4,
                                'dt':round(data2['daily'][3]['temp']['day'] - 273.15,2), 
                                'nt':round(data2['daily'][3]['temp']['night'] - 273.15,2),
                                'desc': data2['daily'][3]['weather'][0]['main'] + ": " +data2['daily'][0]['weather'][0]['description'],
                                'icon':data2['daily'][3]['weather'][0]['icon'],},
                       }
    
    
    return JsonResponse(weather_forcast,safe=False, status=200)


