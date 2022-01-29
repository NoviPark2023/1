from django.urls import path

from real_estate_api.garaze_ponude.views import ListaPonudaGarazaAPIView

app_name = "garaze_ponude"

urlpatterns = [

    # Lista svih Ponuda Garaza
    path('', ListaPonudaGarazaAPIView.as_view(), name='lista_ponuda_garaza'),

    # TODO (Ivana): Implementirati sve URLs po semi iz @see garaze_ponude/views.py
    ## Testirati

]
