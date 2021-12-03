from django.db.backends.ddl_references import Table
from django.db.models import Case, When, Value, F
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Ponude
from .serializers import PonudeSerializer
from ..stanovi.models import Stanovi

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

    def put(self, request, *args, **kwargs):
        """
        Ukoliko se cena Stana razlikuje od cene Stana u Ponudi, automatski se polje
        modela u Ponudama setuje na True ili False.

        * True = Kada se cena razlikuje
        * False = Kada je cena ista

        :param request: Ceo Objekat Ponue u responsu
        :param kwargs: Vraca ID Ponude
        :return: partial_update
        """
        stan = Stanovi.objects.get(id_stana__exact=request.data['stan'])
        ponuda = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])

        if stan.cena_stana == int(request.data['cena_stana_za_kupca']):
            ponuda.odobrenje = False
        else:
            ponuda.odobrenje = True

        stan.save()
        ponuda.save()
        return self.partial_update(request, *args, **kwargs)


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer
