from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from .models import Korisnici
from real_estate_api.korisnici.serializers import KorisniciSerializers


class StandardPaginationKorisnici(PageNumberPagination):
    """Standardna paginacija sa 5 prikaza po stranici za Korisnike"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListaKorisnikaAPIview(generics.ListAPIView):
    """Lista svih korisnika"""
    permission_classes = [IsAuthenticated, ]
    queryset = Korisnici.objects.all().order_by('id')
    serializer_class = KorisniciSerializers
    pagination_class = StandardPaginationKorisnici

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = {
        "username": ["exact"],
    }


class KorisniciDetaljiAPIView(generics.RetrieveAPIView):
    """Get Korisnika po ID-ju, || Detalji Kupca"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class KreirajKorisnika(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    """Kreiranje novog Korisnika"""
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class UrediKorisnika(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    """Uredivanje korisnika po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class ObrisiKoriniska(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    """Brisanje Korinila po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers
