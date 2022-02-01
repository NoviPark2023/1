from django.urls import path

from real_estate_api.garaze.views import *

app_name = "garaze"

urlpatterns = [

    # Lista svih Garaza
    path('', ListaGarazaAPIView.as_view(), name='lista_garaza'),
    # Detalji Garaze
    path('detalji-garaze/<int:id_garaze>/', DetaljiGarazeAPIView.as_view(), name='detalji_garaze'),
    # Kreiranje Garaze
    path('kreiraj-garazu/', KreirajGarazuAPIView.as_view(), name='kreiraj_garazu'),
    # Uredjivanje Garaze
    path('izmeni-garazu/<int:id_garaze>/', UrediGarazuAPIView.as_view(), name='izmeni_garazu'),
    # Brisanje Garaze
    path('obrisi-garazu/<int:id_garaze>/', ObrisiGarazuAPIView.as_view(), name='obrisi_garazu'),

]
