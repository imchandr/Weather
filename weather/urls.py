from django.urls import path
from weather.views import delete_city, home_page, city_weather_details

urlpatterns = [
    path('',home_page, name='city_weather_list'),
    path('<city_name>',city_weather_details, name='city_weather_details'),
    path('delete/<city_name>/',delete_city,name="delete_city"),
]
