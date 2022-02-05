from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.garaze.models import Garaze
from real_estate_api.garaze.serializers import GarazeSerializer
from real_estate_api.garaze.ugovori_garaze.ugovor_garaze import ContractGaraze

lookup_field = 'id_garaze'
lookup_field_kupac = 'id_kupca'


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
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer


class KreirajGarazuAPIView(generics.CreateAPIView):
    """Kreiranje nove Garaze"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field_kupac
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer

    def perform_create(self, serializer):
        """
        Prilikom kreiranja Garaye potrebno je  generisati ili obrisati ugovor.
        Takođe je potrebno postaviti odobrenje(True)  Stana ukoliko je stan
        rezervisan ili prodat.

        :param serializer: GarazeSerializer
        """
        garaza = serializer.save()

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.DOSTUPNA:

            ContractGaraze.delete_contract(garaza)  # Obrisi Ugovor Garaze.


class UrediGarazuAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Garaze po pk-id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer

    def perform_update(self, serializer):
        """
        Prilikom uređivanja statusa Garaže potrebno je  generisati ili obrisati ugovor.

        :param serializer: GarazeSerializer
        """
        garaza = serializer.save()

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.DOSTUPNA:

            ContractGaraze.delete_contract(garaza)  # Obrisi Ugovor Garaze.


class ObrisiGarazuAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Garaze po pk-id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer
