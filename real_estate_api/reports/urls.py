from django.urls import path

from .views import (
    StanoviStatistikaAPIView,
    ReportsProdajaStanovaPoKorisnikuAPIView,
    ReportsProdajaStanovaPoKlijentuAPIView,
)

app_name = "reports"

urlpatterns = [
    path('', StanoviStatistikaAPIView.as_view(), name='index'),
    path('korisnici/', ReportsProdajaStanovaPoKorisnikuAPIView.as_view(), name='index'),
    path('kupci/', ReportsProdajaStanovaPoKlijentuAPIView.as_view(), name='index'),

]
