from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.garaze.models import Garaze
from real_estate_api.garaze.serializers import GarazeSerializer


class ListaGarazaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Garaza.
        * Filtriranje se radi po polju 'jedinstveni_broj_garaze'.
        * Pretraga se radi po polju 'jedinstveni_broj_garaze'.
    """
    permission_classes = [IsAuthenticated]
    queryset = Garaze.objects.all()
    serializer_class = GarazeSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "jedinstveni_broj_garaze": ["exact"],
    }

    search_fields = ['jedinstveni_broj_garaze']


class DetaljiGarazeAPIView(generics.RetrieveAPIView):
    """Lista Garaze po ID-ju, || Detalji Garaze"""
    # TODO(Ivana): View za Detalje jedne Garaze
    ## NEMA KOMPLIKACIJE @see kupci/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass

class UrediGarazuAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Garaze po pk-id"""
    # TODO(Ivana): View za Uredi jednu Garazu
    ## NEMA KOMPLIKACIJE @see kupci/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass

class ObrisiGarazuAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Garaze po pk-id"""
    # TODO(Ivana): View za Obrisi jednu Garazu
    ## NEMA KOMPLIKACIJE @see kupci/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass
