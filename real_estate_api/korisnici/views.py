from rest_framework import generics

from .models import Korisnici
from real_estate_api.korisnici.serializers import KreirajKorisnikaSerializers


class ListaKorisnikaAPIview(generics.ListAPIView):
    """Lista svih korisnika"""
    queryset = Korisnici.objects.all()
    serializer_class = KreirajKorisnikaSerializers


class KorisniciDetaljiAPIView(generics.RetrieveAPIView):
    """Get Korisnika po ID-ju, || Detalji Kupca"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KreirajKorisnikaSerializers


class KreirajKorisnika(generics.CreateAPIView):
    """Kreiranje novog Korisnika"""
    queryset = Korisnici.objects.all()
    serializer_class = KreirajKorisnikaSerializers


class UrediKorisnika(generics.RetrieveUpdateAPIView):
    """Uredivanje korisnika po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KreirajKorisnikaSerializers


class ObrisiKoriniska(generics.RetrieveDestroyAPIView):
    """Brisanje Korinila po id-pk"""
    lookup_field = 'id'
    queryset = Korisnici.objects.all()
    serializer_class = KreirajKorisnikaSerializers
