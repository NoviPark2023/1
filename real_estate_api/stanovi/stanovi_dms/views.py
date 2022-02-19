from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from .models import StanoviDms
from .serializers import (
    StanoviDmsSerializer,
    StanoviUploadDmsSerializer
)

lookup_field = 'id_fajla'


class ListaDokumenaStanoviAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Garaza.
        * Filtriranje se radi po polju 'jedinstveni_broj_garaze'.
        * Pretraga se radi po polju 'jedinstveni_broj_garaze'.
    """
    permission_classes = [IsAuthenticated]
    queryset = StanoviDms.objects.all().order_by('-datum_ucitavanja')
    serializer_class = StanoviDmsSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "naziv_fajla": ["contains"],
    }

    search_fields = ['naziv_fajla']


class DetaljiDokumentaStanaPIView(generics.RetrieveAPIView):
    """Lista Garaze po ID-ju, || Detalji Garaze"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = StanoviDms.objects.all().order_by('-datum_ucitavanja')
    serializer_class = StanoviDmsSerializer


class StanoviDmsUploadAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = StanoviDms.objects.all()
    serializer_class = StanoviUploadDmsSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']
