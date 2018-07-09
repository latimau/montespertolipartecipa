from django import forms
from .models import CoordinateModel, Commenti

from pygeocoder import Geocoder
from pygeolib import GeocoderError

class RequestForm(forms.Form):
    nome = forms.CharField(required=True)
    cognome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True,widget=forms.widgets.Textarea())


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

class CommentiForm(forms.ModelForm):
    class Meta:
        model = Commenti
        fields = ['commento']