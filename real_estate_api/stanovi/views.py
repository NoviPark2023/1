from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import Stanovi, AzuriranjeCena
from .serializers import (
    StanoviSerializer,
    ListaPonudaStanaSerializer,
    BrojPonudaStanaPoMesecimaSerializer,
    AzuriranjeCenaSerializer
)
from real_estate_api.ponude.models import Ponude

lookup_field = 'id_stana'


class ListaStanovaAPIView(generics.ListAPIView):
    """
    API poziv liste svih Stanova.
    ---
        * Filtriranje po poljima:
         - lamela (exact)
         - status_prodaje (exact)
         - sprat (exact)
         - broj_soba (exact)
         - orijentisanost (exact)
         - broj_terasa (exact)
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "lamela": ["icontains"],
        "status_prodaje": ["exact"],
        "sprat": ["exact"],
        "broj_soba": ["exact"],
        "orijentisanost": ["exact"],
        "broj_terasa": ["exact"],
    }


class StanoviDetaljiAPIVIew(generics.RetrieveAPIView):
    """Get Stanovi po ID-ju || DETALJI STANA"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class KreirajStanAPIView(generics.CreateAPIView):
    """Kreiranje novog Stana"""
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class UrediStanViewAPI(generics.RetrieveUpdateAPIView):
    """EDIT Stana poi polju 'id_stana '"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class ObrisiStanViewAPI(generics.RetrieveDestroyAPIView):
    """Brisanje Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class ListaPonudaStanaAPIView(generics.RetrieveAPIView):
    """Lista svih Ponuda Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = ListaPonudaStanaSerializer

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Stanovi.objects.all().filter(stan=id_stana)


class BrojPonudaStanovaPoMesecimaAPIView(generics.ListAPIView):
    """ Broj Ponuda po mesecima za svaki Stan """

    permission_classes = [IsAuthenticated, ]
    serializer_class = BrojPonudaStanaPoMesecimaSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Suma svih ponuda za odredjeni Stan *(kwargs['id_stana']), po mesecima.
        Sabiraju se sve Ponude po mesecima za odredjeni Stan.
        :param request: None
        :param args: None
        :param kwargs: id_stana
        :return: Id stana & Ponude po mesecima za odredjeni Stan
        """
        # #################################
        # BROJ PONUDA PO MESECIMA ZA STAN
        # #################################
        kwargs_field = 'id_stana'

        january = Ponude.objects.filter(datum_ugovora__month=1).filter(stan__id_stana=kwargs[kwargs_field]).count()
        february = Ponude.objects.filter(datum_ugovora__month=2).filter(stan__id_stana=kwargs[kwargs_field]).count()
        march = Ponude.objects.filter(datum_ugovora__month=3).filter(stan__id_stana=kwargs[kwargs_field]).count()
        april = Ponude.objects.filter(datum_ugovora__month=4).filter(stan__id_stana=kwargs[kwargs_field]).count()
        may = Ponude.objects.filter(datum_ugovora__month=5).filter(stan__id_stana=kwargs[kwargs_field]).count()
        june = Ponude.objects.filter(datum_ugovora__month=6).filter(stan__id_stana=kwargs[kwargs_field]).count()
        july = Ponude.objects.filter(datum_ugovora__month=7).filter(stan__id_stana=kwargs[kwargs_field]).count()
        august = Ponude.objects.filter(datum_ugovora__month=8).filter(stan__id_stana=kwargs[kwargs_field]).count()
        september = Ponude.objects.filter(datum_ugovora__month=9).filter(stan__id_stana=kwargs[kwargs_field]).count()
        october = Ponude.objects.filter(datum_ugovora__month=10).filter(stan__id_stana=kwargs[kwargs_field]).count()
        november = Ponude.objects.filter(datum_ugovora__month=11).filter(stan__id_stana=kwargs[kwargs_field]).count()
        december = Ponude.objects.filter(datum_ugovora__month=12).filter(stan__id_stana=kwargs[kwargs_field]).count()

        id_stana = {
            'id_stana': self.kwargs[kwargs_field]
        }

        broj_ponuda_stana_po_mesecima = {
            'broj_ponuda_po_mesecima':
                [
                    {
                        'jan': january,
                        'feb': february,
                        'mart': march,
                        'apr': april,
                        'maj': may,
                        'jun': june,
                        'jul': july,
                        'avg': august,
                        'sep': september,
                        'okt': october,
                        'nov': november,
                        'dec': december,
                    }
                ],
        }

        return Response(id_stana | broj_ponuda_stana_po_mesecima)


# ################################################
# AUTOMATSKO AZURIRANJE CENA STANOVA SERIALIZERS
# ################################################
class AzuriranjeCenaStanaAPIView(generics.ListAPIView):
    """Lista svih cena stanova po deklaraciji Korisnika sistema"""

    permission_classes = [IsAuthenticated, ]
    queryset = AzuriranjeCena.objects.all().order_by('id_azur_cene')
    pagination_class = None
    serializer_class = AzuriranjeCenaSerializer


class AzuriranjeCenaCreateAPIView(generics.CreateAPIView):
    """ Kreiranje mesecne cene kvadrata. """

    permission_classes = [IsAuthenticated, ]
    queryset = AzuriranjeCena.objects.all()
    serializer_class = AzuriranjeCenaSerializer


class AzuriranjeCenaUpdateAPIView(generics.RetrieveUpdateAPIView):
    """ Mesecna izmena cene kvadrata po id-ju. """

    permission_classes = [IsAuthenticated, ]
    queryset = AzuriranjeCena.objects.all()
    serializer_class = AzuriranjeCenaSerializer
    lookup_field = 'id_azur_cene'


class AzuriranjeCenaDeleteAPIView(generics.DestroyAPIView):
    """ Brisanje cena kvadrata po id-ju. """

    permission_classes = [IsAuthenticated, ]
    queryset = AzuriranjeCena.objects.all()
    lookup_field = 'id_azur_cene'
