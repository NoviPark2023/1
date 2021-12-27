from django.urls import path

from .views import (
    ListaStanovaAPIView,
    StanoviDetaljiAPIVIew,
    KreirajStanAPIView,
    UrediStanViewAPI,
    ObrisiStanViewAPI,
    AzuriranjeCena,
    BrojPonudaStanovaPoMesecimaAPIView,
)

app_name = "stanovi"

urlpatterns = [
    # Lista svih Stanova
    path('', ListaStanovaAPIView.as_view(), name='lista_stanova'),
    # Detalji Stana
    path('detalji-stana/<int:id_stana>', StanoviDetaljiAPIVIew.as_view(), name='detalji_stana'),
    # Kreiranje Stana
    path('kreiraj-stan', KreirajStanAPIView.as_view(), name='kreiraj_stan'),
    # Uredjivanje Stana
    path('izmeni-stan/<int:id_stana>', UrediStanViewAPI.as_view(), name='izmeni_stan'),
    # Brisanje Stana
    path('obrisi-stan/<int:id_stana>', ObrisiStanViewAPI.as_view(), name='obrisi_stan'),
    # Kalkulacija cena Stana
    path('kalkulacija-cena-stana/', AzuriranjeCena.as_view(), name='kalkulacija-cena-stana'),
    # Broj Ponuda za Stan po mesecima
    path('ponude-stana-meseci/<int:id_stana>', BrojPonudaStanovaPoMesecimaAPIView.as_view(), name='ponude-stana-meseci')
]
