from django.db.models import OuterRef
from rest_framework import generics

from .models import Ponude
from .serializers import PonudeSerializer

lookup_field = 'id_ponudea'
lookup_field_stan = 'stan'


class ListaPonudaAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

class ListaPonudaZaStanAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id_stana = self.kwargs['stan']
        return Ponude.objects.filter(stan__ponude__id_ponude=id_stana)


class PonudeDetaljiAPIView(generics.RetrieveAPIView):
    """Get Ponude po ID-ju  || Detalji Ponude"""
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class KreirajPonudeuAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude"""
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


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
