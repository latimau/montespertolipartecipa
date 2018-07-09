from django.contrib import admin
from .models import SignUp, CoordinateModel
from .forms import SignUpForm, CoordinateForm
# Register your models here.

class SignUpAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'email', 'timestamp']
    form = SignUpForm
    #class Meta:
    #    model = SignUp
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ['titolo_segnalazione','lat','long']
    form = CoordinateForm


admin.site.register(SignUp, SignUpAdmin)
admin.site.register(CoordinateModel, CoordinateAdmin)