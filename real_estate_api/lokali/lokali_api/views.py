from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.lokali_api.serializers import LokaliSerializer


class ListaLokalaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Lokala.
        * Filtriranje se radi po polju 'jedinstveni_broj_garaze'.
        * Pretraga se radi po polju 'jedinstveni_broj_garaze'.
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

    search_fields = ['lamela_lokala', 'id_lokala']
