from rest_framework import generics

from .models import Kupci
from real_estate_api.kupci.serializers import KupciSerializer, DetaljiKupcaSerializer
from .kupci_pagination import StandardPaginationKupci

lookup_field = 'id_kupca'


class ListaKupacaAPIView(generics.ListAPIView):
    """Lista svih Kupaca"""
    # permission_classes = [IsAuthenticated]
    queryset = Kupci.objects.all()
    serializer_class = KupciSerializer


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
