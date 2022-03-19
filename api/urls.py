import imp
from unicodedata import name
from django.urls import path
from api.views import location_list, location_details

urlpatterns = [
    path('',location_list, name='location_list' ),
    path('<int:id>', location_details, name='location_detail')
]
