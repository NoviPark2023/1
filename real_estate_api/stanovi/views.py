import csv

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Stanovi
from .serializers import (
    StanoviSerializer,
    ListaPonudaStanaSerializer,
    AzuriranjeCenaSerijalizer,
    BrojPonudaStanaPoMesecimaSerializer
)
from ..ponude.models import Ponude

lookup_field = 'id_stana'


class ListaStanovaAPIView(generics.ListAPIView):
    """Lista svih Stanova"""
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all().order_by('id_stana')
    serializer_class = StanoviSerializer


class StanoviDetaljiAPIVIew(generics.RetrieveAPIView):
    """Get Stanovi po ID-ju || DETALJI STANA"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class KreirajStanAPIView(generics.CreateAPIView):
    """Kreiranje novog Stana"""
    permission_classes = [IsAuthenticated, ]
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class UrediStanViewAPI(generics.RetrieveUpdateAPIView):
    """EDIT Stana poi polju 'id_stana '"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
    serializer_class = StanoviSerializer


class ObrisiStanViewAPI(generics.RetrieveDestroyAPIView):
    """Brisanje Stana"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Stanovi.objects.all()
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
        january = Ponude.objects.filter(datum_ugovora__month=1).filter(stan__id_stana=kwargs['id_stana']).count()
        february = Ponude.objects.filter(datum_ugovora__month=2).filter(stan__id_stana=kwargs['id_stana']).count()
        march = Ponude.objects.filter(datum_ugovora__month=3).filter(stan__id_stana=kwargs['id_stana']).count()
        april = Ponude.objects.filter(datum_ugovora__month=4).filter(stan__id_stana=kwargs['id_stana']).count()
        may = Ponude.objects.filter(datum_ugovora__month=5).filter(stan__id_stana=kwargs['id_stana']).count()
        june = Ponude.objects.filter(datum_ugovora__month=6).filter(stan__id_stana=kwargs['id_stana']).count()
        july = Ponude.objects.filter(datum_ugovora__month=7).filter(stan__id_stana=kwargs['id_stana']).count()
        august = Ponude.objects.filter(datum_ugovora__month=8).filter(stan__id_stana=kwargs['id_stana']).count()
        september = Ponude.objects.filter(datum_ugovora__month=9).filter(stan__id_stana=kwargs['id_stana']).count()
        october = Ponude.objects.filter(datum_ugovora__month=10).filter(stan__id_stana=kwargs['id_stana']).count()
        november = Ponude.objects.filter(datum_ugovora__month=11).filter(stan__id_stana=kwargs['id_stana']).count()
        december = Ponude.objects.filter(datum_ugovora__month=12).filter(stan__id_stana=kwargs['id_stana']).count()

        id_stana = {
            'id_stana': self.kwargs['id_stana']
        }

        broj_ponuda_stana_po_mesecima = {'broj_ponuda_po_mesecima':
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


class AzuriranjeCena(generics.ListAPIView):
    """Mesecno azuriranje cena stanova"""
    permission_classes = [IsAuthenticated, ]
    pagination_class = None
    serializer_class = AzuriranjeCenaSerijalizer
    def get(self, request, *args, **kwargs):

        queryset = Stanovi.objects.all()

        file = open('real_estate_api/static/cals-stanovi-cena/AzuriranjeCena.csv')
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:

            for s in queryset:
                # QuerySet data
                sprat = s.sprat
                broj_soba = s.broj_soba
                orijentisanost = s.orijentisanost

                # CSV Data
                sprat_csv : int  = int(row["sprat"])
                broj_soba_csv : float = float(row["broj_soba"])
                orijentisanost_csv : str = row["orijentisanost"]


                if sprat == sprat_csv and broj_soba == broj_soba_csv and orijentisanost == orijentisanost_csv:
                    s.cena_stana = (float(s.kvadratura)*0.97) * float(row["cena_kvadrata"])
                    print(s.id_stana, s.cena_stana)

                    s.save()

            return Response("ISPRAVITI RESPONSE")
