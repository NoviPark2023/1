from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.reports.serializers import (
    ReportsSerializer,
    ProdajaStanovaPoKorisnikuSerializer,
    ProdajaStanovaPoKlijentuSerializer,
)
from real_estate_api.stanovi.models import Stanovi
from rest_framework.response import Response


class StanoviStatistikaAPIView(generics.ListAPIView):
    """Lista svih Stanova"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportsSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        TODO: Komentar
        """

        stanovi_global_ukupno = Stanovi.objects.all().count()
        stanovi_ukupan_broj = Stanovi.objects.aggregate(ukupno_stanova=Count('id_stana'))

        # ###################################
        # REPORTS STANOVA PO STATUSU PRODAJE
        # ###################################
        ukuno_stanovi_rezervisan = Stanovi.objects.filter(status_prodaje='rezervisan').aggregate(
            rezervisano=Count('id_stana'))
        ukuno_stanovi_dostupan = Stanovi.objects.filter(status_prodaje='dostupan').aggregate(dostupan=Count('id_stana'))
        ukuno_stanovi_prodat = Stanovi.objects.filter(status_prodaje='prodat').aggregate(prodat=Count('id_stana'))

        # ###################################
        # REPORTS STANOVA PO STATUSU PRODAJE U %
        # ###################################
        stanovi_rezervisano_procenti = (ukuno_stanovi_rezervisan.get('rezervisano') / stanovi_global_ukupno) * 100
        print(stanovi_rezervisano_procenti)
        stanovi_dostupan_procenti = (ukuno_stanovi_dostupan.get('dostupan') / stanovi_global_ukupno) * 100
        print(stanovi_dostupan_procenti)
        stanovi_prodati_procenti = (ukuno_stanovi_prodat.get('prodat') / stanovi_global_ukupno) * 100
        print(stanovi_prodati_procenti)

        stanovi_agregirano_procenti = {
            'procenat_rezervisan': stanovi_rezervisano_procenti,
            'procenat_dostupan': stanovi_dostupan_procenti,
            'procenat_prodat': stanovi_prodati_procenti
        }

        # ###################################
        # PRODAJA PO MESECIMA
        # ###################################
        january = Ponude.objects.filter(datum_ugovora__month=1).filter(status_ponude='kupljen').count()
        february = Ponude.objects.filter(datum_ugovora__month=2).filter(status_ponude='kupljen').count()
        march = Ponude.objects.filter(datum_ugovora__month=3).filter(status_ponude='kupljen').count()
        april = Ponude.objects.filter(datum_ugovora__month=4).filter(status_ponude='kupljen').count()
        may = Ponude.objects.filter(datum_ugovora__month=5).filter(status_ponude='kupljen').count()
        june = Ponude.objects.filter(datum_ugovora__month=6).filter(status_ponude='kupljen').count()
        july = Ponude.objects.filter(datum_ugovora__month=7).filter(status_ponude='kupljen').count()
        august = Ponude.objects.filter(datum_ugovora__month=8).filter(status_ponude='kupljen').count()
        september = Ponude.objects.filter(datum_ugovora__month=9).filter(status_ponude='kupljen').count()
        october = Ponude.objects.filter(datum_ugovora__month=10).filter(status_ponude='kupljen').count()
        november = Ponude.objects.filter(datum_ugovora__month=11).filter(status_ponude='kupljen').count()
        december = Ponude.objects.filter(datum_ugovora__month=12).filter(status_ponude='kupljen').count()
        prodaja_po_mesecima = {'prodaja_po_mesecima':
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

        agregacioni_api = stanovi_ukupan_broj | \
                          ukuno_stanovi_rezervisan | \
                          ukuno_stanovi_dostupan | \
                          ukuno_stanovi_prodat | \
                          stanovi_agregirano_procenti | \
                          prodaja_po_mesecima
        return Response(agregacioni_api)


class ReportsProdajaStanovaPoKorisnikuAPIView(generics.ListAPIView):
    """Broj svih rezervisanih Stanova po Korisniku (Agentu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Korisnici.objects.all()
    serializer_class = ProdajaStanovaPoKorisnikuSerializer
    pagination_class = None


class ReportsProdajaStanovaPoKlijentuAPIView(generics.ListAPIView):
    """Broj svih rezervisanih Stanova po Klijentu (Kupcu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Kupci.objects.all()
    serializer_class = ProdajaStanovaPoKlijentuSerializer
    pagination_class = None
