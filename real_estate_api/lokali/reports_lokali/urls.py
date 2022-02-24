from django.urls import path

from .views import (
    LokaliStatistikaAPIView,
    ReportsProdajaLokalaPoKorisnikuAPIView,
    ReportsProdajaLokalaPoKlijentuAPIView,
    RoiLokalaAPIView,
)

app_name = "reports_lokali"

urlpatterns = [
    path('', LokaliStatistikaAPIView.as_view(), name='reports-lokali'),

    path('korisnici/', ReportsProdajaLokalaPoKorisnikuAPIView.as_view(), name='reports-lokali-po-korisniku'),

    path('kupci/', ReportsProdajaLokalaPoKlijentuAPIView.as_view(), name='reports-lokali-po-klijentu'),

    path('roi/', RoiLokalaAPIView.as_view(), name='reports-roi'),

]
