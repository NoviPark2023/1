from django.urls import path

from real_estate_api.lokali.lokali_api.views import (
    ListaLokalaAPIView,
    DetaljiLokalaAPIVIew,
    KreirajLokalAPIView,
    UrediLokalViewAPI,
    ObrisiLokalViewAPI,
    BrojPonudaLokalaPoMesecimaAPIView
)

app_name = "lokali"

urlpatterns = [
    # Lista svih Lokala
    path('', ListaLokalaAPIView.as_view(), name='lista_lokala'),

    # Detalji Lokala
    path('detalji-lokala/<int:id_lokala>/', DetaljiLokalaAPIVIew.as_view(), name='detalji_lokala'),

    # Kreiranje Lokala
    path('kreiraj-lokal/', KreirajLokalAPIView.as_view(), name='kreiraj_lokal'),

    # Uredjivanje Lokala
    path('izmeni-lokal/<int:id_lokala>/', UrediLokalViewAPI.as_view(), name='izmeni_lokal'),

    # Brisanje Lokala
    path('obrisi-lokal/<int:id_lokala>/', ObrisiLokalViewAPI.as_view(), name='obrisi_lokal'),

    # Broj Ponuda za Lokal po mesecima
    path('ponude-lokala-meseci/<int:id_lokala>', BrojPonudaLokalaPoMesecimaAPIView.as_view(),
         name='ponude-lokala-meseci'),

]
