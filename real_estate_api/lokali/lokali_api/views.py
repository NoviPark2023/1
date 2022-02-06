from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.lokali_api.serializers import LokaliSerializer
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer

lookup_field = 'id_lokala'


class ListaLokalaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Lokala.
        * Filtriranje se radi po polju 'id_lokala'.
        * Pretraga se radi po poljima 'lamela_lokala', 'id_lokala'.
    """
    permission_classes = [IsAuthenticated]
    queryset = Lokali.objects.all()
    serializer_class = LokaliSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "id_lokala": ["exact"],
    }

    search_fields = ['lamela_lokala']


class DetaljiLokalaAPIVIew(generics.RetrieveAPIView):
    """Get Lokali po ID-ju || DETALJI LOKALA"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by('id_lokala')
    serializer_class = LokaliSerializer


class KreirajLokalAPIView(generics.CreateAPIView):
    """Kreiranje novog Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by('id_lokala')
    serializer_class = LokaliSerializer


class UrediLokalViewAPI(generics.RetrieveUpdateAPIView):
    """EDIT Lokala poi polju 'id_lokala '"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by('id_lokala')
    serializer_class = LokaliSerializer


class ObrisiLokalViewAPI(generics.RetrieveDestroyAPIView):
    """Brisanje Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by('id_lokala')
    serializer_class = LokaliSerializer


class ListaPonudaLokalaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by(lookup_field)
    serializer_class = PonudeLokalaSerializer

    def get_queryset(self):
        id_lokala = self.kwargs['id_lokala']
        return Lokali.objects.all().filter(id_lokala=id_lokala)
