from rest_framework import generics

from .models import Stanovi
from .serializers import StanoviSerializer
from .stanovi_paginacija import StandardPaginationStanovi

lookup_field = 'id_stana'


class ListaStanovaAPIView(generics.ListAPIView):
    """Lista svih Stanova"""
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class ListaStanovaPaginationAPIView(ListaStanovaAPIView):
    """Lista svih Stanova sa paginacijom"""
    pagination_class = StandardPaginationStanovi


class StanoviDetaljiAPIVIew(generics.RetrieveAPIView):
    """Get Stanovi po ID-ju || DETALJI STANA"""
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class KreirajStanAPIView(generics.CreateAPIView):
    """Kreiranje novog Stana"""
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class UrediStanViewAPI(generics.RetrieveUpdateAPIView):
    """EDIT Stana poi polju 'id_stana '"""
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class ObrisiStanViewAPI(generics.RetrieveDestroyAPIView):
    """Brisanje Stana"""
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer
