from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer

lookup_field = 'id_ponude_lokala'
lookup_field_lokal = 'id_lokala'


class ListaPonudaLokalaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Ponuda Lokala.
        * Filtriranje se radi po polju 'id_ponude_lokala'.
        * Pretraga se radi po poljima 'lamela_lokala', 'id_lokala'.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = PonudeLokala.objects.all().order_by(lookup_field)
    serializer_class = PonudeLokalaSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "id_ponude_lokala": ["exact"],
    }

    search_fields = ['id_ponude_lokala']


class DetaljiPonudeLokalaAPIView(generics.RetrieveAPIView):
    """Get Ponude Lokala po ID-ju  || Detalji Ponude Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all()
    serializer_class = PonudeLokalaSerializer


class KreirajPonuduLokalaAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_lokal = lookup_field_lokal
    queryset = PonudeLokala.objects.all().order_by('id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer


class IzmeniPonuduLokalaAPIView(generics.RetrieveUpdateAPIView):
    """Izmena Ponude Lokala po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all().order_by('id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer


class ObrisiPonuduLokalaAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude Lokala po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all().order_by('-id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer
