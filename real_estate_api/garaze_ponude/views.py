from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.garaze_ponude.models import GarazePonude
from real_estate_api.garaze_ponude.serializers import PonudeGarazaSerializer

lookup_field = 'id_ponude_garaze'

class ListaPonudaGarazaAPIView(generics.ListAPIView):
    """Lista svih Ponuda Garaza"""
    permission_classes = [IsAuthenticated, ]
    queryset = GarazePonude.objects.all().order_by(lookup_field)
    serializer_class = PonudeGarazaSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "id_ponude_garaze": ["exact"],
    }

    search_fields = ['id_ponude_garaze', 'kupac_garaze__ime_prezime']


class DetaljiPonudeGarazeAPIView(generics.RetrieveAPIView):
    """Lista Garaze po ID-ju, || Detalji Garaze"""
    # TODO(Ivana): View za Detalje jedne Ponude Garaze
    ## NEMA KOMPLIKACIJE @see ponude/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass

class UrediPonuduGarazeAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Garaze po pk-id"""
    # TODO(Ivana): View za Uredi jednu Ponude Garaze
    ## NEMA KOMPLIKACIJE @see ponude/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass

class ObrisiPonuduGarazeAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Garaze po pk-id"""
    # TODO(Ivana): View za Obrisi jednu Ponude Garaze
    ## NEMA KOMPLIKACIJE @see ponude/views.py
    ## Obrisati komentare kada se zavrsi
    ## Testirati
    pass
