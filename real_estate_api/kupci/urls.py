from django.urls import path

from .views import (
    ListaKupacaAPIView,
    KupciDetaljiAPIView,
    KreirajKupcaAPIView,
    UrediKupcaAPIView,
    ObrisiKupcaAPIView,
    ListaKupacaPoImenuAPIView,
    ListaPonudaKupcaAPIView,
)

app_name = "kupci"

urlpatterns = [

    # Lista svih Kupaca
    path('', ListaKupacaAPIView.as_view(), name='lista_kupaca'),
    # Lista kupaca autocomplete po imenu
    path('kupci-autocomplete/<str:ime_prezime>/', ListaKupacaPoImenuAPIView.as_view(),
         name='lista_kupaca_po_imenu_autocomplete'),
    # Detalji Kupca
    path('detalji-kupca/<int:id_kupca>/', KupciDetaljiAPIView.as_view(), name='detalji_kupca'),
    # Uredjivanje Kupaca
    path('izmeni-kupca/<int:id_kupca>/', UrediKupcaAPIView.as_view(), name='izmeni_kupca'),
    # Brisanje Kupca
    path('obrisi-kupca/<int:id_kupca>/', ObrisiKupcaAPIView.as_view(), name='obrisi_kupca'),
    # Kreiranje Kupca
    path('kreiraj-kupca/', KreirajKupcaAPIView.as_view(), name='kreiraj_kupca'),
    # Lista Ponuda Kupca
    path('lista-ponuda-kupca/<int:id_kupca>/', ListaPonudaKupcaAPIView.as_view(), name='lista_ponuda_kupca'),
]
