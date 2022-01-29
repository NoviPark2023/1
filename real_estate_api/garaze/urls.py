from django.urls import path

from real_estate_api.garaze.views import ListaGarazaAPIView

app_name = "garaze"

urlpatterns = [

    # Lista svih Garaza
    path('', ListaGarazaAPIView.as_view(), name='lista_garaza'),

    # TODO (Ivana): Implementirati sve URLs po semi iz @see garaze/views.py
    ## Testirati

]
