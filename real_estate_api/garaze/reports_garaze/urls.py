from django.urls import path
from .views import GarazeStatistikaAPIView


app_name = "reports-garaze"

urlpatterns = [
    path('', GarazeStatistikaAPIView.as_view(), name='reports-garaze'),
]
