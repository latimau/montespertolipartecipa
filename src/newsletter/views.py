from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import CoordinateModel
from .forms import SignUpForm, ContactForm, CoordinateForm

from pygeocoder import Geocoder
from geojson import Feature, Point, FeatureCollection

#server_immagini = 'http://52.28.48.112/media/'
server_immagini = 'http://139.191.148.108:8000/media/'

#folder_immagini = '/var/www/html/test_site.com/static_in_env/media_root/uploaded_images/'
folder_immagini = '/var/www/html/trydjango18/static_in_env/media_root/uploaded_images/'
# Create your views here.
def home(request):

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        full_name = form.cleaned_data.get('full_name')
        if not full_name:
            full_name = 'None'
        instance.full_name = full_name
        instance.save()
    context = {'form':form}
    return render(request,'home.html',context)

def contact(request):
    form = ContactForm(request.POST or None)

    if form.is_valid():
        form_email = form.cleaned_data.get('email')
        form_messge = form.cleaned_data.get('message')
        form_full_name = form.cleaned_data.get('full_name')

        subject = 'Test prova Django'
        contact_message = '%s: %s via %s'%(form_full_name, form_email, form_messge)
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, form_email]

        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

    context = {'form':form}
    return render(request,'forms.html', context)

@login_required
def coordinate(request):
    lat = ''
    long = ''

    if request.method == 'POST':
        form = CoordinateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            #una volta salvato i dati nel DB chiamo la funzione per ridimensionare le immagini
            handle_uploaded_image(request.FILES['image'])
            return redirect('/segnalazioni/')

    else:
        form = CoordinateForm()

    context = {'form':form,'lat':lat,'long':long}

    return render(request,'coordinate.html', context)

def segnalazioni(request):
    query_decoro = CoordinateModel.objects.filter(tipo_segnalazione='decoro')
    query_sicurezza = CoordinateModel.objects.filter(tipo_segnalazione='sicurezza')
    query_strada = CoordinateModel.objects.filter(tipo_segnalazione='strada')

    feature_decoro = []
    feature_sicurezza = []
    feature_strada = []

    #leggo le entry nel DB e creo le features in geoJson basandomi sulle entries
    for result in query_decoro:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_decoro.append(feature)

    for result in query_sicurezza:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_sicurezza.append(feature)

    for result in query_strada:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_strada.append(feature)

    #una volta create le varie features creo la featurecollection in geoJson
    featureCollection_decoro = FeatureCollection(feature_decoro)
    featureCollection_strada = FeatureCollection(feature_strada)
    featureCollection_sicurezza = FeatureCollection(feature_sicurezza)


    context = {'featureCollection_decoro':featureCollection_decoro, 'featureCollection_strada':featureCollection_strada, 'featureCollection_sicurezza':featureCollection_sicurezza}
    return render(request,'map.html', context)

#ridimensiono le immagini inserite
def handle_uploaded_image(i):
    import PIL
    from PIL import Image

    basewidth = 280
    img = Image.open(folder_immagini+str(i))
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save(folder_immagini+str(i))