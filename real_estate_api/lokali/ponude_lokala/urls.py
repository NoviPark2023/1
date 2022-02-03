from django.urls import path

from real_estate_api.lokali.ponude_lokala.views import ListaPonudaLokalaAPIView

app_name = "lokali"

urlpatterns = [
    # Lista svih Ponuda Lokala
    path('', ListaPonudaLokalaAPIView.as_view(), name='lista_ponuda_lokala'),

]
