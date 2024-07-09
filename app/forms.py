from django import forms 
class Contactinfo(forms.Form):
   COUNTRY_CHOICES = [
        ('+91', '+91 (India)'),
        ('+1', '+1(United  States)'),
    ]
   countrycode=forms.ChoiceField(choices=COUNTRY_CHOICES, initial='+91')
   mobileno=forms.CharField(max_length=15)
   email=forms.EmailField()

from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

from .models import flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = flight
        fields = '__all__'        
