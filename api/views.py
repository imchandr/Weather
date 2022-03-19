from telnetlib import RSP
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Location
from api.serlializers import LocationSerializer

@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        location = Location.objects.all()
        location_srlzr = LocationSerializer(location, many=True)
        return Response(location_srlzr.data)
    
    elif request.method == 'POST':
        location_srlzr = LocationSerializer(data = request.data)
        if location_srlzr.is_valid():
            location_srlzr.save()
            return Response(location_srlzr.data, status=status.HTTP_201_CREATED)
        return Response(location_srlzr.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def location_details(request, id):
    try:
        location = Location.objects.get(id = id)
    except Location.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        location_srlzr = LocationSerializer(location)
        return Response(location_srlzr.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        location_srlzr = LocationSerializer(location, data=request.data)
        if location_srlzr.is_valid():
            location_srlzr.save()
            return Response(location_srlzr.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
