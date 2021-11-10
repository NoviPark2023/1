from rest_framework import generics

from .models import Kupci
from real_estate_api.kupci.serializers import KupciSerializer, DetaljiKupcaSerializer
from .kupci_pagination import StandardPaginationKupci
from dal import autocomplete

lookup_field = 'id_kupca'


class ListaKupacaAPIView(generics.ListAPIView):
    """Lista svih Kupaca"""
    # permission_classes = [IsAuthenticated]
    queryset = Kupci.objects.all().order_by('id_kupca')
    serializer_class = KupciSerializer


class ListaKupacaPoImenuAPIView(generics.ListAPIView):
    serializer_class = KupciSerializer

    def get_queryset(self):
        queryset = Kupci.objects.all()
        ime_prezime = self.kwargs['ime_prezime']
        if self.kwargs:
            queryset = queryset.filter(ime_prezime__icontains=ime_prezime) # 'icontains' case-insensitive
        return queryset


class ListaKupacaPaginationAPIView(ListaKupacaAPIView):
    """Lista svih Kupaca sa paginacijom"""
    pagination_class = StandardPaginationKupci


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
