from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Kupci
from real_estate_api.kupci.serializers import KupciSerializer, DetaljiKupcaSerializer, ListaPonudaKupcaSerializer
from ..ponude.models import Ponude

lookup_field = 'id_kupca'


class StandardPaginationKupci(PageNumberPagination):
    """Standart paginacija sa 5 prikaza po stranici za Kupce"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListaKupacaAPIView(generics.ListAPIView):
    """Lista svih Kupaca"""
    # permission_classes = [IsAuthenticated]
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer
    pagination_class = StandardPaginationKupci


class ListaKupacaPoImenuAPIView(generics.ListAPIView):
    """Autocomplete sitem za pretragu Kupaca"""
    serializer_class = KupciSerializer

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = Kupci.objects.all()
        ime_prezime: str = self.kwargs['ime_prezime']
        if self.kwargs:
            queryset = queryset.filter(ime_prezime__icontains=ime_prezime)  # 'icontains' case-insensitive
        return queryset


class KupciDetaljiAPIView(generics.RetrieveAPIView):
    """Get Kupci po ID-ju, || Detalji Kupca"""

    # permission_classes = [IsAuthenticated]

    lookup_field = lookup_field
    queryset = Kupci.objects.all()
    serializer_class = DetaljiKupcaSerializer


class KreirajKupcaAPIView(generics.CreateAPIView):
    """Kreiranje novog Kupca"""
    # permission_classes = [IsAuthenticated]
    queryset = Kupci.objects.all()
    serializer_class = KupciSerializer


class UrediKupcaAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Kupca po pk-id"""
    # permission_classes = [IsAuthenticated]
    lookup_field = lookup_field
    queryset = Kupci.objects.all()
    serializer_class = KupciSerializer


class ObrisiKupcaAPIView(generics.RetrieveDestroyAPIView):
    """Obrisi Kupa po id"""
    # permission_classes = [IsAuthenticated]
    lookup_field = lookup_field
    queryset = Kupci.objects.all()
    serializer_class = KupciSerializer


class ListaPonudaKupcaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Kupca"""
    # permission_classes = [IsAuthenticated]
    lookup_field = lookup_field
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = ListaPonudaKupcaSerializer
    pagination_class = StandardPaginationKupci

    def get_queryset(self):
        id_kupca = self.kwargs['id_kupca']
        return Ponude.objects.all().filter(kupac=id_kupca)
