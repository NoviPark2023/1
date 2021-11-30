from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Stanovi
from .serializers import StanoviSerializer, ListaPonudaStanaSerializer

lookup_field = 'id_stana'


class StandardPaginationStanovi(PageNumberPagination):
    """Standardna paginacija sa 5 prikaza po srtanici za Stanove"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListaStanovaAPIView(generics.ListAPIView):
    """Lista svih Stanova"""
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer
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


class ListaPonudaStanaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Stana"""
    # permission_classes = [IsAuthenticated]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = ListaPonudaStanaSerializer
    pagination_class = StandardPaginationStanovi

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Stanovi.objects.all().filter(stan=id_stana)
