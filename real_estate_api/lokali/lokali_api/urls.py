from django.urls import path

from real_estate_api.lokali.lokali_api.views import ListaLokalaAPIView

app_name = "lokali"

urlpatterns = [

    # Lista svih Lokala
    path('', ListaLokalaAPIView.as_view(), name='lista_lokala'),


]
