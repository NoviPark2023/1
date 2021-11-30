from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Ponude
from .serializers import PonudeSerializer

lookup_field = 'id_ponude'
lookup_field_stan = 'id_stana'


class StandardPaginationPonude(PageNumberPagination):
    """Standardna paginacija sa 5 prikaza po stranici za Ponude"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListaPonudaAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    queryset = Ponude.objects.all().order_by(lookup_field)
    serializer_class = PonudeSerializer
    pagination_class = StandardPaginationPonude


class ListaPonudaZaStanAPIView(ListaPonudaAPIView):
    """Lista svih Ponuda"""
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Ponuda for
        the Stan as determined by the Stan ID portion of the URL.
        """
        id_stana = self.kwargs['id_stana']

        return Ponude.objects.all().filter(stan=id_stana)


class PonudeDetaljiAPIView(generics.RetrieveAPIView):
    """Get Ponude po ID-ju  || Detalji Ponude"""
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class KreirajPonudeuAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude"""
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)


class UrediPonuduViewAPI(generics.RetrieveUpdateAPIView):
    """Urednjivanje Ponude po ID-ju"""
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer
