from django.urls import path

from .views import (
    ListaKorisnikaAPIview,
    KreirajKorisnika,
    KorisniciDetaljiAPIView,
    UrediKorisnika,
    ObrisiKoriniska,
)

# Registrovan AUTH_USER_MODEL = 'korisnici.Korisnici' u Django Config
app_name = "korisnici"

urlpatterns = [
    # Lista svih Korisnika
    path('', ListaKorisnikaAPIview.as_view(), name='lista_korisnika'),
    # Kreiranje Korisnika
    path('kreiraj-korisnika/', KreirajKorisnika.as_view(), name='kreiraj_korisnika'),
    # Detalji Korisnika
    path('detalji-korisnika/<int:id>/', KorisniciDetaljiAPIView.as_view(), name='detalji_korisnika'),
    # Uredjivanje Korisnika
    path('izmeni-korisnika/<int:id>/', UrediKorisnika.as_view(), name='izmeni_korisnika'),
    # Brisanje Korisnika
    path('obrisi-korisnika/<int:id>/', ObrisiKoriniska.as_view(), name='obrisi_korisnika')
]
