from dataclasses import field
from importlib.metadata import files
from django import forms
from api.models import Location
from weather.models import City

class CityForm(forms.ModelForm):
    name = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = City
        fields = ['name'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].choices = [(city.name, city.name) for city in Location.objects.all()]
        
    

        