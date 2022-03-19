from django.db.models import fields
from rest_framework import serializers

from api.models import Location

from api.models import Location

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    lat = serializers.CharField()
    long = serializers.CharField()
    
    def create(self, validated_data):
        return Location.objects.create(**validated_data)
    
    def update(sef, instance, validates_data):
        instance.name = validates_data.get('name', instance.name)
        instance.lat = validates_data.get('lat', instance.name)
        instance.long = validates_data.get('long', instance.name)
        instance.save()
        return instance
        