from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ListaPonudaAPIView,
    ListaPonudaZaStanAPIView,
    KreirajPonudeuAPIView,
    ObrisiPonuduAPIView,
    PonudeDetaljiAPIView,
    UrediPonuduViewAPI, FileDownloadListAPIView,

)

app_name = "ponude"

urlpatterns = [
    # Lista svih Ponuda
    path('', ListaPonudaAPIView.as_view(), name='lista_ponuda'),
    # Lista Ponuda filtriranih po 'ID STANA'
    path('lista-ponuda-stana/<int:id_stana>/', ListaPonudaZaStanAPIView.as_view(), name='lista_ponuda_za_stan'),
    # Detalji Ponude
    path('detalji-ponude/<int:id_ponude>/', PonudeDetaljiAPIView.as_view(), name='detalji_ponude'),
    # Uredi Ponudu
    path('izmeni-ponudu/<int:id_ponude>/', UrediPonuduViewAPI.as_view(), name='izmeni_ponudu'),
    # Obrisi Ponudu
    path('obrisi-ponudu/<int:id_ponude>/', ObrisiPonuduAPIView.as_view(), name='obrisi_ponudu'),
    # Kreiraj Ponudu
    path('kreiraj-ponudu/', KreirajPonudeuAPIView.as_view(), name='kreiraj_ponudu'),
    path('download/<int:id_ponude>/', FileDownloadListAPIView.as_view())

]
