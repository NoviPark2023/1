from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.lokali_api.models import Lokali
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

    def perform_create(self, serializer):
        """
        Prilikom kreiranja Ponude Lokala potrebno je  generisati
        ili obrisati ugovor. Takođe je potrebno postaviti odobrenje(True)
        Lokala ukoliko je lokal rezervisan ili prodat.

        :param serializer: PonudeLokalaSerializer
        """
        ponuda_lokala = serializer.save()

        if ponuda_lokala.status_ponude == PonudeLokala.StatusPonudeLokala.REZERVISAN:

            # Kreiranje Ugovora
            Contract.create_contract(ponuda_lokala, ponuda_lokala.lokal, ponuda_lokala.kupac)

            ponuda_lokala.lokal.status_prodaje_lokala = Lokali.StatusProdajeLokala.REZERVISAN
            ponuda_lokala.lokal.save()
            ponuda_lokala.odobrenje = True
            ponuda_lokala.klijent_prodaje_lokala = self.request.user  # Set klijenta prodaje Lokala
            ponuda_lokala.save()

        elif ponuda_lokala.status_prodaje_lokala == Lokali.StatusPonude.KUPLJEN:

            # Kreiranje Ugovora
            Contract.create_contract(ponuda, ponuda.stan, ponuda.kupac)

            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.PRODAT
            ponuda.stan.save()
            ponuda.odobrenje = True
            ponuda.klijent_prodaje = self.request.user  # Set klijenta prodaje Stana
            ponuda.save()

    #     elif ponuda.status_ponude == Ponude.StatusPonude.POTENCIJALAN:
    #         ponuda.stan.status_prodaje = Stanovi.StatusProdaje.DOSTUPAN
    #         ponuda.stan.save()
    #         ponuda.odobrenje = False
    #         ponuda.save()
    #
    # def get_queryset(self):
    #     # Potrebno za prikaz svih Ponuda samo za odredjeni Stan
    #     id_stana = self.kwargs['id_stana']
    #     return Ponude.objects.all().filter(stan=id_stana)


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
