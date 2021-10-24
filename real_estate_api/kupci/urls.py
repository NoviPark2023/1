from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ListaKupacaAPIView,
    KupciDetaljiAPIView,
    KreirajKupcaAPIView,
    UrediKupcaAPIView,
    ObrisiKupcaAPIView
)

app_name = "kupci"

urlpatterns = [
    # PREUZIM API TOKEN
    path('api/token/', obtain_auth_token, name='obtain-token'),
    # Lista svih Kupaca
    path('', ListaKupacaAPIView.as_view(), name='lista_kupaca'),
    # Detalji Kupca
    path('detalji-kupca/<int:id_kupca>/', KupciDetaljiAPIView.as_view(), name='detalji_kupca'),
    # Uredjivanje Kupaca
    path('uredi-kupca/<int:id_kupca>/', UrediKupcaAPIView.as_view(), name='uredi_kupca'),
    # Brisanje Kupca
    path('obrisi-kupca/<int:id_kupca>/', ObrisiKupcaAPIView.as_view(), name='obrisi_kupca'),
    # Kreiranje Kupca
    path('kreiraj-kupca/', KreirajKupcaAPIView.as_view(), name='kreiraj_kupca'),
]
