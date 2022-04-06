from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from rest_framework.settings import api_settings

from .models import Kupci
from real_estate_api.kupci.serializers import (
    KupciSerializer,
    DetaljiKupcaSerializer,
    ListaPonudaKupcaSerializer
)
from ..ponude.models import Ponude

lookup_field = 'id_kupca'


class ListaKupacaAPIView(generics.ListAPIView):
    """
    Lista svih Kupaca
    ---
    Filtriranje po poljima:
     - lice
     - ime_prezime
     - email
     - broj_telefona
     - Jmbg_Pib
     - adresa
    """
    permission_classes = [IsAuthenticated]
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "lice": ["exact"],
        "ime_prezime": ["icontains"],
        "email": ["icontains"],
        "broj_telefona": ["icontains"],
        "Jmbg_Pib": ["icontains"],
        "adresa": ["icontains"],
    }


class ListaKupacaPoImenuAPIView(generics.ListAPIView):
    """Autocomplete sitem za pretragu Kupaca"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = KupciSerializer

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = Kupci.objects.all()
        ime_prezime: str = self.kwargs['ime_prezime']
        if self.kwargs:
            queryset = queryset.filter(ime_prezime__icontains=ime_prezime)  # 'icontains' case-insensitive
        return queryset


class KupciDetaljiAPIView(generics.RetrieveAPIView):
    """Get Kupci po ID-ju, || Detalji Kupca"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = DetaljiKupcaSerializer


class KreirajKupcaAPIView(generics.CreateAPIView):
    """Kreiranje novog Kupca"""
    permission_classes = [IsAuthenticated, ]
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer


class UrediKupcaAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Kupca po pk-id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer


class ObrisiKupcaAPIView(generics.RetrieveDestroyAPIView):
    """Obrisi Kupa po id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer


class ListaPonudaKupcaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Kupca"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = ListaPonudaKupcaSerializer

    def get_queryset(self):
        id_kupca = self.kwargs['id_kupca']
        return Ponude.objects.all().filter(kupac=id_kupca)
