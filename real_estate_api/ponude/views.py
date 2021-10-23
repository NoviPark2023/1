from rest_framework import generics

from .models import Ponude
from .serializers import PonudeSerializer

lookup_field = 'id_ponude'


class ListaPonudaAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


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
