# forms.py
from django import forms

class WeatherForm(forms.Form):
    city = forms.CharField(label='도시명', max_length=100)
