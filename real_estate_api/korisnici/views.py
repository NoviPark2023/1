from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Korisnici
from .korisnici_pagination import StandardPaginationKorisnici
from real_estate_api.korisnici.serializers import KorisniciSerializers


class ListaKorisnikaAPIview(generics.ListAPIView):
    """Lista svih korisnika"""
    queryset = Korisnici.objects.all().order_by('id')
    serializer_class = KorisniciSerializers


class ListaKorisnikaPaginationAPIView(ListaKorisnikaAPIview):
    """Lista svih Stanova sa paginacijom"""
    pagination_class = StandardPaginationKorisnici


class KorisniciDetaljiAPIView(generics.RetrieveAPIView):
    """Get Korisnika po ID-ju, || Detalji Kupca"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class KreirajKorisnika(generics.CreateAPIView):
    """Kreiranje novog Korisnika"""
    permission_classes = [AllowAny]
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class UrediKorisnika(generics.RetrieveUpdateAPIView):
    """Uredivanje korisnika po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers


class ObrisiKoriniska(generics.RetrieveDestroyAPIView):
    """Brisanje Korinila po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KorisniciSerializers
