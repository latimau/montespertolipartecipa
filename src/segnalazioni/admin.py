from django.contrib import admin

from .models import CoordinateModel, Commenti
from .forms import CoordinateForm
# Register your models here.

class CoordinateAdmin(admin.ModelAdmin):
    list_display = ['titolo_segnalazione','lat','long']
    form = CoordinateForm

class CommentiAdmin(admin.ModelAdmin):
    list_display = ['commento','user','pubblicato']
    list_filter = ['pubblicato']


admin.site.register(CoordinateModel, CoordinateAdmin)
admin.site.register(Commenti, CommentiAdmin)