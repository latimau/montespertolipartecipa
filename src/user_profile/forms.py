from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from .models import Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    #birth_date = forms.DateField(widget=SelectDateWidget())
    class Meta:
        model = Profile
        fields = ['bio','location','birth_date']