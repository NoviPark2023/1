from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.response import Response

from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.lokali_api.serializers import LokaliSerializer, BrojPonudaLokalaPoMesecimaSerializer
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala

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
    """Lista svih Ponuda Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Lokali.objects.all().order_by(lookup_field)
    serializer_class = PonudeLokalaSerializer

    def get_queryset(self):
        id_lokala = self.kwargs['id_lokala']
        return Lokali.objects.all().filter(id_lokala=id_lokala)


class BrojPonudaLokalaPoMesecimaAPIView(generics.ListAPIView):
    """ Broj Ponuda po mesecima za svaki Lokal """
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = BrojPonudaLokalaPoMesecimaSerializer

    def get(self, request, *args, **kwargs):
        """
        Suma svih ponuda za odredjeni Lokal *(kwargs['id_lokala']), po mesecima.
        Sabiraju se sve Ponude po mesecima za odredjeni Lokal.
        :param request: None
        :param args: None
        :param kwargs: id_lokala
        :return: Id Lokala & Ponude po mesecima za odredjeni Lokal
        """
        # #################################
        # BROJ PONUDA PO MESECIMA ZA LOKAL
        # #################################
        kwargs_field = 'id_lokala'

        january = PonudeLokala.objects.filter(datum_ugovora_lokala__month=1).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        february = PonudeLokala.objects.filter(datum_ugovora_lokala__month=2).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        march = PonudeLokala.objects.filter(datum_ugovora_lokala__month=3).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        april = PonudeLokala.objects.filter(datum_ugovora_lokala__month=4).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        may = PonudeLokala.objects.filter(datum_ugovora_lokala__month=5).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        june = PonudeLokala.objects.filter(datum_ugovora_lokala__month=6).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        july = PonudeLokala.objects.filter(datum_ugovora_lokala__month=7).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        august = PonudeLokala.objects.filter(datum_ugovora_lokala__month=8).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        september = PonudeLokala.objects.filter(datum_ugovora_lokala__month=9).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        october = PonudeLokala.objects.filter(datum_ugovora_lokala__month=10).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        november = PonudeLokala.objects.filter(datum_ugovora_lokala__month=11).filter(lokali__id_lokala=kwargs[kwargs_field]).count()
        december = PonudeLokala.objects.filter(datum_ugovora_lokala__month=12).filter(lokali__id_lokala=kwargs[kwargs_field]).count()

        id_lokala = {
            'id_lokala': self.kwargs[kwargs_field]
        }

        broj_ponuda_lokala_po_mesecima = {
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

        return Response(id_lokala | broj_ponuda_lokala_po_mesecima)
