import csv

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Stanovi
from .serializers import StanoviSerializer, ListaPonudaStanaSerializer, AzuriranjeCenaSerijalizer

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


class AzuriranjeCena(generics.ListAPIView):
    """Mesecno azuriranje cena stanova"""

    def get(self, request, *args, **kwargs):
        queryset = Stanovi.objects.all()
        serializer_class = AzuriranjeCenaSerijalizer

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
