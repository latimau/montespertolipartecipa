from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', home, name='home'),
    url(r'^inserimento_segnalazione/$', inserimento_segnalazione, name='inserimento'),
    url(r'^segnalazioni/$', segnalazioni, name='segnalazioni'),
    url(r'^dettaglio_segnalazione/(?P<segnalazione_id>\d+)/$', segnalazioni_dettaglio, 
        name='dettaglio_segnalazione'),
    url(r'^dettaglio_categoria/(?P<categoria_tipo>\w+)/$', dettaglio_categoria, 
        name='dettaglio_categoria'),
    url(r'^segnala_categoria/$', segnala_categoria, name='segnala_categoria'),
    url(r'^richiesta_ok/$', richiesta_ok, name='richiesta_ok'),
    url(r'^pubblica_commento/(?P<id_commento>\d+)/$', pubblica_commento, name='pubblica_commento'),

    
 
]
