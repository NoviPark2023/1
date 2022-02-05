from django.urls import path

from real_estate_api.lokali.ponude_lokala.views import *

app_name = "lokali"

urlpatterns = [
    # Lista svih Ponuda Lokala
    path('', ListaPonudaLokalaAPIView.as_view(), name='lista_ponuda_lokala'),

    # Lista Ponuda Lokala filtriranih po 'ID LOKALA'
    path('lista-ponuda-lokala/<int:id_lokala>/', ListaPonudaLokalaAPIView.as_view(), name='lista_ponuda_za_lokal'),

    # Detalji Ponude Lokala
    path('detalji-ponude-lokala/<int:id_ponude_lokala>/',
         DetaljiPonudeLokalaAPIView.as_view(), name='detalji_ponude_lokala'),

    # Kreiraj Ponudu Lokala
    path('kreiraj-ponudu-lokala/', KreirajPonuduLokalaAPIView.as_view(), name='kreiraj_ponudu_lokala'),

    # Obrisi Ponudu
    path('obrisi-ponudu-lokala/<int:id_ponude_lokala>/', ObrisiPonuduLokalaAPIView.as_view(), name='obrisi_ponudu_lokala'),
]
