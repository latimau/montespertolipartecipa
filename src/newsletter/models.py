from django.db import models

# Create your models here.
class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.email

TIPO_SEGNALAZIONE = (
    ('decoro', 'Decoro Urbano'),
    ('strada', "Qualita' della strada"),
    ('sicurezza', 'Sicurezza'),
)

QUALITA_SEGNALAZIONE = (
    ('positiva', '+'),
    ('negativa', "-"),
    ('neutra', '+/-'),
)

class CoordinateModel(models.Model):
    titolo_segnalazione = models.CharField(max_length=150)
    desc_segnalazione = models.TextField(blank=True, null=True)
    tipo_segnalazione = models.CharField(max_length=100, choices=TIPO_SEGNALAZIONE, default='decoro')
    qualita_segnalazione = models.CharField(max_length=100, choices=QUALITA_SEGNALAZIONE, default='positiva')
    lat = models.DecimalField(max_digits=19, decimal_places=10)
    long = models.DecimalField(max_digits=19, decimal_places=10)
    image = models.ImageField(upload_to='uploaded_images/', blank=True, null=True)

    def __unicode__(self):
        return self.titolo_segnalazione