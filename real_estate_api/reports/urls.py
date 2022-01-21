from django.urls import path

from .views import (
    StanoviStatistikaAPIView,
    ReportsProdajaStanovaPoKorisnikuAPIView,
    ReportsProdajaStanovaPoKlijentuAPIView,
    RoiStanovaAPIView,
)

app_name = "reports"

urlpatterns = [
    path('', StanoviStatistikaAPIView.as_view(), name='reports'),
    path('korisnici/', ReportsProdajaStanovaPoKorisnikuAPIView.as_view(), name='reports-stanovi-po-korisniku'),
    path('kupci/', ReportsProdajaStanovaPoKlijentuAPIView.as_view(), name='reports-stanovi-po-klijentu'),
    path('roi/', RoiStanovaAPIView.as_view(), name='reports-roi'),

]
