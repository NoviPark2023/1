from django.urls import path

from .views import (
    ListaKupacaAPIView,
    KupciDetaljiAPIView,
    KreirajKupcaAPIView,
    UrediKupcaAPIView,
    ObrisiKupcaAPIView
)

app_name = "kupci"

urlpatterns = [

    # Lista svih Kupaca
    path('', ListaKupacaAPIView.as_view(), name='lista_kupaca'),
    # Detalji Kupca
    path('detalji-kupca/<int:id_kupca>/', KupciDetaljiAPIView.as_view(), name='detalji_kupca'),
    # Uredjivanje Kupaca
    path('izmeni-kupca/<int:id_kupca>/', UrediKupcaAPIView.as_view(), name='izmeni_kupca'),
    # Brisanje Kupca
    path('obrisi-kupca/<int:id_kupca>/', ObrisiKupcaAPIView.as_view(), name='obrisi_kupca'),
    # Kreiranje Kupca
    path('kreiraj-kupca/', KreirajKupcaAPIView.as_view(), name='kreiraj_kupca'),
]
