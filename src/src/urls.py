from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from segnalazioni import views as seg
from user_profile import views as up
from src import views as src

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', seg.home, name='home'),
    url(r'^inserimento_segnalazione/$', seg.inserimento_segnalazione, name='inserimento'),
    url(r'^segnalazioni/$', seg.segnalazioni, name='segnalazioni'),
    url(r'^dettaglio_segnalazione/(?P<segnalazione_id>\d+)/$', seg.segnalazioni_dettaglio, 
         name='dettaglio_segnalazione'),
    url(r'^dettaglio_categoria/(?P<categoria_tipo>\w+)/$', seg.dettaglio_categoria, 
         name='dettaglio_categoria'),
    url(r'^segnala_categoria/$', seg.segnala_categoria, name='segnala_categoria'),
    url(r'^richiesta_ok/$', seg.richiesta_ok, name='richiesta_ok'),
    url(r'^pubblica_commento/(?P<id_commento>\d+)/$', seg.pubblica_commento, name='pubblica_commento'),
    url(r'^user_profile/$', up.update_profile, name='user_profile'),
    url(r'^cookie/$', src.cookie, name='cookie'),
    url(r'^progetto/$', src.progetto, name='progetto'),
    url(r'^heatmap/$', src.heatmap, name='heatmap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)