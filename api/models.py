from unittest.util import _MAX_LENGTH
from django.db import models

class Location(models.Model):
    
    name = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    long = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
