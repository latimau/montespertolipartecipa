from django import forms
from .models import SignUp, CoordinateModel

from pygeocoder import Geocoder
from pygeolib import GeocoderError

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields =['full_name','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split('@')
        domain, extension = provider.split('.')
        if not extension == "edu":
            raise forms.ValidationError('Please use a valid EDU address')
        return email

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()


class CoordinateForm(forms.ModelForm):
    class Meta:
        model = CoordinateModel
        fields = ['titolo_segnalazione','lat','long','desc_segnalazione','tipo_segnalazione','qualita_segnalazione','image']

    #def clean_indirizzo(self):
    #    indirizzo = self.cleaned_data.get('indirizzo')
    #    try:
    #        indirizzo = Geocoder.geocode(indirizzo)
    #    except GeocoderError:
    #        raise forms.ValidationError("The address entered could not be geocoded")

    #    return indirizzo
