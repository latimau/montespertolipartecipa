from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CoordinateModel, Commenti
from .forms import RequestForm, CoordinateForm, CommentiForm

from pygeocoder import Geocoder
from geojson import Feature, Point, FeatureCollection

from datetime import datetime, timedelta

####AMAZON SETTINGS############################################################################
#server_immagini = 'http://52.28.48.112/media/'
#folder_immagini= '/var/www/html/test_site.com/static_in_env/media_root/'
#folder_immagini_big = '/var/www/html/test_site.com/static_in_env/media_root/uploaded_images/'
####END AMAZON SETTINGS########################################################################

###########DEVELOPEMENT SETTINGS###############################################################
server_immagini = 'http://127.0.0.1:8000/media/'
folder_immagini_big = '/Users/Maurizio/Desktop/test_django_18/montespertolipartecipa/static_in_env/media_root/uploaded_images/'
folder_immagini = '/Users/Maurizio/Desktop/test_django_18/montespertolipartecipa/static_in_env/media_root/'
link_pubblica_commento = '127.0.0.1:8000/pubblica_commento/'
###########END DEVELOPEMENT SETTINGS############################################################

# Create your views here.
def home(request):

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    query_decoro = CoordinateModel.objects.filter(tipo_segnalazione='decoro')
    query_sicurezza = CoordinateModel.objects.filter(tipo_segnalazione='sicurezza')
    query_strada = CoordinateModel.objects.filter(tipo_segnalazione='strada')
    query_traffico = CoordinateModel.objects.filter(tipo_segnalazione='traffico')

    feature_decoro = []
    feature_sicurezza = []
    feature_strada = []
    feature_traffico = []

    #mi calcolo la data da passare come filtro alla query
    today = datetime.today()
    delta = timedelta(days=30)

    difference = today - delta

    #prendo le prime 12 segnalazioni piu' recenti di 30 giorni
    query_tot = CoordinateModel.objects.filter(timestamp__gte = difference)[:12]

    #leggo le entry nel DB e creo le features in geoJson basandomi sulle entries
    for result in query_decoro:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_decoro.append(feature)

    for result in query_sicurezza:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_sicurezza.append(feature)

    for result in query_strada:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_strada.append(feature)

    for result in query_traffico:
        lat = float(result.lat)
        long = float(result.long)
        my_point = Point((long,lat))

        if result.image:
            img = server_immagini+str(result.image)
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione,'image':img}
        else:
            my_point_properties = {'id':result.id,'titolo_segnalazione':result.titolo_segnalazione, 'desc_segnalazione':result.desc_segnalazione,'tipo_segnalazione':result.tipo_segnalazione,'qualita_segnalazione':result.qualita_segnalazione}

        feature = Feature(geometry=my_point,properties=my_point_properties)
        feature_traffico.append(feature)

    #una volta create le varie features creo la featurecollection in geoJson
    featureCollection_decoro = FeatureCollection(feature_decoro)
    featureCollection_strada = FeatureCollection(feature_strada)
    featureCollection_sicurezza = FeatureCollection(feature_sicurezza)
    featureCollection_traffico = FeatureCollection(feature_traffico)


    context = {'value':'home','num_visits':num_visits,'featureCollection_traffico':featureCollection_traffico,
    'featureCollection_decoro':featureCollection_decoro, 'featureCollection_strada':featureCollection_strada, 
    'featureCollection_sicurezza':featureCollection_sicurezza, 'query_tot':query_tot, 
    'server_immagini':server_immagini}
    return render(request,'map.html', context)


@login_required
def inserimento_segnalazione(request):
    lat = ''
    long = ''

    if request.method == 'POST':
        form = CoordinateForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            #una volta salvato i dati nel DB chiamo la funzione per ridimensionare le immagini
            if 'image' in request.FILES:
                query = CoordinateModel.objects.get(id=instance.id)
                handle_uploaded_image(query.image)
                handle_uploaded_image2(query.image)

            messages.success(request, 'Segnalazione correttamente inserita!')
            return redirect('/')

        else:
            messages.error(request, 'La segnalazione non puo\' essere inserita.Per favore correggi gli errori sottostanti')

    else:
        form = CoordinateForm()

    context = {'form':form,'lat':lat,'long':long,'value':'inserimento'}

    return render(request,'coordinate.html', context)


#ridimensiono le immagini inserite
def handle_uploaded_image2(i):
    import PIL
    from PIL import Image

    basewidth = 250
    hsize = 250
    img = Image.open(folder_immagini+str(i))
    wpercent = (basewidth / float(img.size[0]))
    #hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

    img.save(folder_immagini+str(i))

def handle_uploaded_image(i):
    import PIL
    from PIL import Image

    basewidth = 600

    img = Image.open(folder_immagini+str(i))
    #wpercent = (basewidth / float(img.size[0]))
    #hsize = int((float(img.size[1]) * float(wpercent)))
    #img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

    img.save(folder_immagini_big+"big/"+str(i), quality=95)

def segnalazioni(request):

    query_tot = CoordinateModel.objects.all()

    context = {'query_tot':query_tot,'server_immagini':server_immagini, 'value':'elenco'}
    return render(request,'segnalazioni.html', context)

def segnalazioni_dettaglio(request,segnalazione_id):
    message = ''
    feature_segnalazione = []
    query_dett_segnalazione = CoordinateModel.objects.get(id=segnalazione_id)

    if query_dett_segnalazione.tipo_segnalazione == 'decoro':
        categoria = 'Decoro Urbano'

    if query_dett_segnalazione.tipo_segnalazione == 'strada':
        categoria = "Qualita'/Sicurezza Stradale"

    if query_dett_segnalazione.tipo_segnalazione == 'sicurezza':
        categoria = 'Sicurezza del Cittadino'

    if query_dett_segnalazione.tipo_segnalazione == 'traffico':
        categoria = 'Traffico'


    # questo lo faccio per far apparire il punto sulla mappa
    lat = float(query_dett_segnalazione.lat)
    long = float(query_dett_segnalazione.long)
    my_point = Point((long,lat))

    my_point_properties = {'id':query_dett_segnalazione.id,'tipo_segnalazione':query_dett_segnalazione.tipo_segnalazione,'qualita_segnalazione':query_dett_segnalazione.qualita_segnalazione}

    feature = Feature(geometry=my_point,properties=my_point_properties)
    feature_segnalazione.append(feature)

    featureCollection = FeatureCollection(feature_segnalazione)
    lat = str(lat).replace(',','.')
    long = str(long).replace(',','.')

    ############inserimento commenti alla segnalazione###############################################
    id = ''
    form = CommentiForm(request.POST or None)
    #recupero i commenti per la segnalazione
    query_commenti = Commenti.objects.filter(segnalazione=segnalazione_id, pubblicato='Y').order_by('-data_commento')
    num_commenti = query_commenti.count()

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        commento = form.cleaned_data.get('commento')
        instance.segnalazione = CoordinateModel.objects.get(id=segnalazione_id)
        instance.save()
        id = instance.id
        #message = "Il commento inserito e' in fase di moderazione. Grazie da parte del team di MontespertoliPartecipa."

        messages.success(request, "Il commento inserito e' in fase di moderazione. Grazie da parte del team di MontespertoliPartecipa.")
        link_pubblica_commento = '127.0.0.1:8000/pubblica_commento/'+str(id)+'/'

        #una volta inserito il commento invio una email per segnalare un nuovo commento inserito

        subject = 'MONTESPERTOLI PARTECIPA - Inserito un nuvo commento per la segnalazione %s' %(instance.segnalazione.titolo_segnalazione)
        contact_message = 'E\' stato inserito un nuovo commento alla segnalazione da titolo: %s. \nIl commento inserito e\' il seguente: %s. \nPer pubblicare il commento clicca il seguente link:%s' %(instance.segnalazione.titolo_segnalazione, commento, link_pubblica_commento)
        from_email = request.user.email
        to_email = [settings.EMAIL_HOST_USER]

        #send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

        context = {'id':id,'form':form, 'query':query_dett_segnalazione, 'categoria':categoria, 
        'server_immagini':server_immagini, 'featureCollection':featureCollection,'lat':lat, 'long':long, 
        'query_commenti':query_commenti, 'num_commenti':num_commenti}
        return render(request,'dettaglio_segnalazione.html', context)

    context = {'id':id,'form':form, 'query':query_dett_segnalazione, 'categoria':categoria, 
    'server_immagini':server_immagini, 'featureCollection':featureCollection,'lat':lat, 'long':long, 
    'query_commenti':query_commenti, 'num_commenti':num_commenti}
    return render(request,'dettaglio_segnalazione.html', context)

def dettaglio_categoria(request,categoria_tipo):
    if categoria_tipo == 'decoro':
        categoria = 'Decoro Urbano'

    if categoria_tipo == 'strada':
        categoria = "Qualita'/Sicurezza Stradale"

    if categoria_tipo == 'sicurezza':
        categoria = 'Sicurezza del Cittadino'

    if categoria_tipo == 'traffico':
        categoria = 'Traffico'

    query_dett_categoria = CoordinateModel.objects.filter(tipo_segnalazione=categoria_tipo)
    context = {'query':query_dett_categoria, 'categoria': categoria, 'server_immagini':server_immagini}
    return render(request,'dettaglio_categoria.html', context)

@login_required
def segnala_categoria(request):
    form = RequestForm(request.POST or None)

    if form.is_valid():
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_nome = form.cleaned_data.get('nome')
        form_cognome = form.cleaned_data.get('cognome')

        subject = 'MONTESPERTOLI PARTECIPA - Richiesta di una nuova categoria da %s %s' %(form_nome, form_cognome)
        contact_message = '%s'%(form_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, form_email]

        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

        return redirect('/richiesta_ok/')

    context = {'form':form}
    return render(request,'richiesta_categoria.html', context)

def richiesta_ok(request):
    message = "La richiesta e' stata inoltrata con successo, grazie."
    context = {'message':message}
    return render(request,'risposta.html', context)

#@login_required
#def commenta_segnalazione(request,segnalazione_id):
#
#     tit_segnalazione = CoordinateModel.objects.get(id = segnalazione_id)
#
#     tit_segnalazione = tit_segnalazione.titolo_segnalazione
#
#     form = CommentiForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.segnalazione = CoordinateModel.objects.get(id=segnalazione_id)
#         instance.save()
#
#         return redirect('/commento_ok/')
#     #una volta inserito il commento deve essere inviata una email per la moderazione
#     context = {'form':form, 'tit_segnalazione':tit_segnalazione}
#     return render(request,'commenta_segnalazione.html', context)
#
# def commento_ok(request):
#     message = "Il commento e' stato correttamente pubblicato"
#     context = {'message':message}
#     return render(request,'risposta.html', context)

#funzione che viene attivata quando si clicca sul link inviato per email
def pubblica_commento(request,id_commento):
    commento = Commenti.objects.get(id=id_commento)
    commento.pubblicato = 'Y'
    commento.save()
    message = "Il commento e' stato correttamente pubblicato"
    context = {'message':message}
    return render(request,'risposta.html', context)
