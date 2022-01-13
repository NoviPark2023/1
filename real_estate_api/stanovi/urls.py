from django.urls import path

from .views import (
    ListaStanovaAPIView,
    StanoviDetaljiAPIVIew,
    KreirajStanAPIView,
    UrediStanViewAPI,
    ObrisiStanViewAPI,
    BrojPonudaStanovaPoMesecimaAPIView,
    AzuriranjeCenaCreateAPIView,
    AzuriranjeCenaUpdateAPIView,
    AzuriranjeCenaDeleteAPIView,
    AzuriranjeCenaStanaAPIView,
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
    # Broj Ponuda za Stan po mesecima
    path('ponude-stana-meseci/<int:id_stana>', BrojPonudaStanovaPoMesecimaAPIView.as_view(), name='ponude-stana-meseci'),
    # Lista svih mesecnih cena kvadrata
    path('listing-cena-kvadrata', AzuriranjeCenaStanaAPIView.as_view(), name='lista-cena-kvadrata'),
    # Kreiranje mesecne cene kvadrata
    path('kreiraj-cenu-kvadrata', AzuriranjeCenaCreateAPIView.as_view(), name='kreiraj-cenu-kvadrata'),
    # Promena mesecne cene kvadrata
    path('promeni-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaUpdateAPIView.as_view(), name='promeni-cenu-kvadrata'),
    # Brisanje mesecne cene kvadrata
    path('izbrisi-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaDeleteAPIView.as_view(), name='izbrisi-cenu-kvadrata')
]
