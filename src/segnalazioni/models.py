from django.db import models
from django.contrib.auth.models import User
from time import time


TIPO_SEGNALAZIONE = (
    ('decoro', 'Decoro Urbano'),
    ('strada', "Qualita' della strada"),
    ('sicurezza', 'Sicurezza del cittadino'),
    ('traffico', 'Traffico'),
)

QUALITA_SEGNALAZIONE = (
    ('positiva', '+'),
    ('negativa', "-"),
    ('neutra', '+/-'),
)

YN = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

def get_upload_filename(instance,filename):
    return "uploaded_images/%s_%s" % (str(time()).replace('.','_'),filename)

#segnalazioni
class CoordinateModel(models.Model):
    titolo_segnalazione = models.CharField(max_length=150)
    desc_segnalazione = models.TextField(blank=True, null=True)
    tipo_segnalazione = models.CharField(max_length=100, choices=TIPO_SEGNALAZIONE, default='decoro')
    qualita_segnalazione = models.CharField(max_length=100, choices=QUALITA_SEGNALAZIONE, default='positiva')
    lat = models.DecimalField(max_digits=19, decimal_places=10)
    long = models.DecimalField(max_digits=19, decimal_places=10)
    image = models.ImageField(upload_to=get_upload_filename, blank=True, null=True)
    user = models.ForeignKey(User)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = "Segnalazioni"
        verbose_name_plural = "Segnalazioni"

class Commenti(models.Model):
    commento = models.TextField()
    user = models.ForeignKey(User)
    segnalazione = models.ForeignKey(CoordinateModel)
    data_commento = models.DateTimeField(auto_now_add=True, auto_now=False)
    pubblicato = models.CharField(max_length=1, choices=YN, default='N')

    class Meta:
        verbose_name = "Commenti"
        verbose_name_plural = "Commenti"