from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ListaKorisnikaAPIview,
    KreirajKorisnika,
    KorisniciDetaljiAPIView,
    UrediKorisnika,
    ObrisiKoriniska

)

app_name = "korisnici"

urlpatterns = [
    # Lista svih Korisnika
    path('', ListaKorisnikaAPIview.as_view(), name='lista_korisnika'),
    # Kreiranje Korisnika
    path('kreiraj-korisnika/', KreirajKorisnika.as_view(), name='kreiraj_korisnika'),
    # Detalji Korisnika
    path('detalji-korisinka/<int:id>/', KorisniciDetaljiAPIView.as_view(), name='detalji_korisnika'),
    # Uredjivanje Korisnika
    path('izmeni-korisnika/<int:id>/', UrediKorisnika.as_view(), name='izmeni_korisnika'),
    # Brisanje Korisnika
    path('obrisi-korisnika/<int:id>/', ObrisiKoriniska.as_view(), name='obrisi_korisnika')
]
