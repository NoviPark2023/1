from babel.numbers import format_decimal, parse_decimal
from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.reports_lokali.serializers import (
    ReportsLokaliSerializer,
    ProdajaLokalaPoKorisnikuSerializer,
    ProdajaLokalaPoKlijentuSerializer,
    RoiSerializer,
)


class LokaliStatistikaAPIView(generics.ListAPIView):
    """ Kreiranje izvestaja za entitet 'LOKALI' """

    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportsLokaliSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Kreiranje izvestaja po kriterijumima:
            * LOKALI PO STATUSU PRODAJE
            * LOKALI PO STATUSU PRODAJE %
            * PRODAJA LOKALA PO MESECIMA
            * BROJ PONUDA LOKALA PO MESECIMA
        ---
        :param request: None
        :param args: None
        :param kwargs: None
        :return: Resposne 'agregacioni_api' gorespomenutih kriterijumima
        """
        lokali_global_ukupno = Lokali.objects.all().count()
        lokali_ukupan_broj = Lokali.objects.aggregate(ukupno_lokala=Count('id_lokala'))

        # ########################################
        # REPORTS LOKALA PO STATUSU PRODAJE REPORT
        # ########################################
        ukupno_lokala_rezervisanih = Lokali.objects.filter(
            status_prodaje_lokala=Lokali.StatusProdajeLokala.REZERVISAN
        ).aggregate(
            rezervisano=Count('id_lokala')
        )
        ukupno_lokala_dostupnih = Lokali.objects.filter(
            status_prodaje_lokala=Lokali.StatusProdajeLokala.DOSTUPAN
        ).aggregate(
            dostupno=Count('id_lokala')
        )
        ukupno_lokala_prodatih = Lokali.objects.filter(
            status_prodaje_lokala=Lokali.StatusProdajeLokala.PRODAT
        ).aggregate(
            prodato=Count('id_lokala')
        )

        # ############################################
        # REPORTS LOKALA PO STATUSU PRODAJE U % REPORT
        # ############################################
        try:
            lokali_rezervisano_procenti = (ukupno_lokala_rezervisanih.get('rezervisano') / lokali_global_ukupno) * 100
            lokali_dostupno_procenti = (ukupno_lokala_dostupnih.get('dostupno') / lokali_global_ukupno) * 100
            lokali_prodato_procenti = (ukupno_lokala_prodatih.get('prodato') / lokali_global_ukupno) * 100
        except ZeroDivisionError:
            lokali_rezervisano_procenti = 0
            lokali_dostupno_procenti = 0
            lokali_prodato_procenti = 0

        lokali_agregirano_procenti = {
            # Zaokruziti procente na 2 decimale
            'procenat_rezervisanih': round(lokali_rezervisano_procenti, 2),
            'procenat_dostupnih': round(lokali_dostupno_procenti, 2),
            'procenat_prodatih': round(lokali_prodato_procenti, 2)
        }

        # ####################################
        # PRODAJA LOKALA PO MESECIMA REPORT
        # ####################################
        january = PonudeLokala.objects.filter(datum_ugovora_lokala__month=1).filter(status_ponude_lokala='kupljen').count()
        february = PonudeLokala.objects.filter(datum_ugovora_lokala__month=2).filter(status_ponude_lokala='kupljen').count()
        march = PonudeLokala.objects.filter(datum_ugovora_lokala__month=3).filter(status_ponude_lokala='kupljen').count()
        april = PonudeLokala.objects.filter(datum_ugovora_lokala__month=4).filter(status_ponude_lokala='kupljen').count()
        may = PonudeLokala.objects.filter(datum_ugovora_lokala__month=5).filter(status_ponude_lokala='kupljen').count()
        june = PonudeLokala.objects.filter(datum_ugovora_lokala__month=6).filter(status_ponude_lokala='kupljen').count()
        july = PonudeLokala.objects.filter(datum_ugovora_lokala__month=7).filter(status_ponude_lokala='kupljen').count()
        august = PonudeLokala.objects.filter(datum_ugovora_lokala__month=8).filter(status_ponude_lokala='kupljen').count()
        september = PonudeLokala.objects.filter(datum_ugovora_lokala__month=9).filter(status_ponude_lokala='kupljen').count()
        october = PonudeLokala.objects.filter(datum_ugovora_lokala__month=10).filter(status_ponude_lokala='kupljen').count()
        november = PonudeLokala.objects.filter(datum_ugovora_lokala__month=11).filter(status_ponude_lokala='kupljen').count()
        december = PonudeLokala.objects.filter(datum_ugovora_lokala__month=12).filter(status_ponude_lokala='kupljen').count()

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

        # #################################
        # BROJ PONUDA PO MESECIMA REPORT
        # #################################
        january = PonudeLokala.objects.filter(datum_ugovora_lokala__month=1).count()
        february = PonudeLokala.objects.filter(datum_ugovora_lokala__month=2).count()
        march = PonudeLokala.objects.filter(datum_ugovora_lokala__month=3).count()
        april = PonudeLokala.objects.filter(datum_ugovora_lokala__month=4).count()
        may = PonudeLokala.objects.filter(datum_ugovora_lokala__month=5).count()
        june = PonudeLokala.objects.filter(datum_ugovora_lokala__month=6).count()
        july = PonudeLokala.objects.filter(datum_ugovora_lokala__month=7).count()
        august = PonudeLokala.objects.filter(datum_ugovora_lokala__month=8).count()
        september = PonudeLokala.objects.filter(datum_ugovora_lokala__month=9).count()
        october = PonudeLokala.objects.filter(datum_ugovora_lokala__month=10).count()
        november = PonudeLokala.objects.filter(datum_ugovora_lokala__month=11).count()
        december = PonudeLokala.objects.filter(datum_ugovora_lokala__month=12).count()

        broj_ponuda_po_mesecima = {'broj_ponuda_po_mesecima':
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

        # #####################
        # RAST PRODAJE REPORT
        # #####################
        january = PonudeLokala.objects.filter(datum_ugovora_lokala__month=1).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0
        february = PonudeLokala.objects.filter(datum_ugovora_lokala__month=2).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        march = PonudeLokala.objects.filter(datum_ugovora_lokala__month=3).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        april = PonudeLokala.objects.filter(datum_ugovora_lokala__month=4).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        may = PonudeLokala.objects.filter(datum_ugovora_lokala__month=5).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        june = PonudeLokala.objects.filter(datum_ugovora_lokala__month=6).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        july = PonudeLokala.objects.filter(datum_ugovora_lokala__month=7).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        august = PonudeLokala.objects.filter(datum_ugovora_lokala__month=8).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        september = PonudeLokala.objects.filter(datum_ugovora_lokala__month=9).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        october = PonudeLokala.objects.filter(datum_ugovora_lokala__month=10).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        november = PonudeLokala.objects.filter(datum_ugovora_lokala__month=11).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        december = PonudeLokala.objects.filter(datum_ugovora_lokala__month=12).filter(
            status_ponude_lokala=PonudeLokala.StatusPonudeLokala.KUPLJEN).aggregate(
            ukupna_suma_prodatih_lokala=Sum('cena_lokala_za_kupca')
        )['ukupna_suma_prodatih_lokala'] or 0

        ukupna_suma_prodatih_lokala = {'ukupna_suma_prodatih_lokala':
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

        agregacioni_api = (
            lokali_ukupan_broj |
            ukupno_lokala_rezervisanih |
            ukupno_lokala_dostupnih |
            ukupno_lokala_prodatih |
            lokali_agregirano_procenti |
            prodaja_po_mesecima |
            broj_ponuda_po_mesecima |
            ukupna_suma_prodatih_lokala
        )
        return Response(agregacioni_api, content_type="application/json")


class ReportsProdajaLokalaPoKorisnikuAPIView(generics.ListAPIView):
    """ Broj svih rezervisanih Lokala po Korisniku (Agentu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Korisnici.objects.all()
    serializer_class = ProdajaLokalaPoKorisnikuSerializer
    pagination_class = None


class ReportsProdajaLokalaPoKlijentuAPIView(generics.ListAPIView):
    """ Broj svih rezervisanih Lokala po Klijentu (Kupcu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Kupci.objects.all()
    serializer_class = ProdajaLokalaPoKlijentuSerializer
    pagination_class = None


class RoiLokalaAPIView(generics.ListAPIView):
    """ Return on investment za Lokale Report"""

    permission_classes = [IsAuthenticated, ]
    serializer_class = RoiSerializer
    pagination_class = None

    @staticmethod
    def suma_lokala_po_lameli(lamela_lokala: str) -> str:
        """
        Lokali se razvrstavaju po Lamelama, ukupno ih ima 3 i to:
            * L1.0.zz  ||  L2.0.zz  || L3.0.zz
        Strukutra oznake Lamela je:
            * XX.Y.ZZ Ceo hash Lamele
            * XX: Broj Lamela  ||  Y: Broj Sprata  ||  ZZ: Broj Lokala
        Podrazumevana spratnost je prizemlje (0), osim ako klijent ne odredi drugacije
        ---
        :param lamela: str: 'lamela__startswith' -> naziv lamele *(npr. L1.1).
        :return: str: Formatirana (decimal) suma cene lokala po lameli.
        """
        svi_lokali_po_lameli = Lokali.objects.values('cena_lokala').filter(
            lamela_lokala__startswith=lamela_lokala).aggregate(Sum('cena_lokala'))

        # Format decimala za sumu cene Lokala
        if svi_lokali_po_lameli['cena_lokala__sum'] is not None:
            svi_lokali_po_lameli = format_decimal(
                svi_lokali_po_lameli['cena_lokala__sum'],
                locale='sr_RS')
        else:
            svi_lokali_po_lameli = 0

        return svi_lokali_po_lameli

    def get(self, request, *args, **kwargs):
        """
        Agregacija APIja za ROI lokala i to po kriterijumu:
            * Ukupna kvadratura Lokala

        :param request: None
        :param args: None
        :param kwargs: None
        :return: agregacioni_api za ROI
        """
        # ###############
        # UKUPNO KVADRATA
        # ###############
        # Suma Kvadrata
        lokali_ukupno_kvadrata = Lokali.objects.aggregate(
            lokali_ukupno_kvadrata=Sum('kvadratura_lokala')
        )

        # Za kalkulaciju u kvadratima Decimal
        lokali_ukupno_kvadrata_float = lokali_ukupno_kvadrata

        # Format decimal places for 'lokali_ukupno_kvadrata'
        lokali_ukupno_kvadrata = format_decimal(
            lokali_ukupno_kvadrata['lokali_ukupno_kvadrata'],
            locale='sr_RS')

        # Return API Structure 'kvadratura_lokala'
        kvadratura_lokala = {
            'kvadratura_lokala':
                {
                    'lokali_ukupno_kvadrata': lokali_ukupno_kvadrata
                }
        }

        # ################
        # SUMA CENE LOKALA
        # ################
        # LAMELA: PRIZEMLJE LAMELA 1 (L1.0)
        svi_lokali_po_lameli_l1_0 = self.suma_lokala_po_lameli('L1.0')

        # LAMELA: PRIZEMLJE LAMELA 2 (L2.0)
        svi_lokali_po_lameli_l2_0 = self.suma_lokala_po_lameli('L2.0')

        # LAMELA: PRIZEMLJE LAMELA 3 (L3.0)
        svi_lokali_po_lameli_l3_0 = self.suma_lokala_po_lameli('L3.0')

        # Return API Structure 'ukupna_suma_lokala_po_lameli'
        ukupna_suma_lokala_po_lameli = {
            'ukupna_cena_lokala_po_lamelama':
                {
                    'svi_lokali_po_lameli_l1_0': svi_lokali_po_lameli_l1_0,
                    'svi_lokali_po_lameli_l2_0': svi_lokali_po_lameli_l2_0,
                    'svi_lokali_po_lameli_l3_0': svi_lokali_po_lameli_l3_0
                }
        }

        # ###################################
        # UKUPNA SUMA CENE LOKALA PO LAMELAMA
        # ###################################
        # Ukupna suma cene Lokala po Lameli L1
        ukupna_suma_cena_lamela_l1 = self.suma_lokala_po_lameli('L1')

        # Ukupna suma cene Lokala po Lameli L2
        ukupna_suma_cena_lamela_l2 = self.suma_lokala_po_lameli('L2')

        # Ukupna suma cene Lokala po Lameli L3
        ukupna_suma_cena_lamela_l3 = self.suma_lokala_po_lameli('L3')

        # #######################
        # UKUPNA SUMA CENE LOKALA
        # #######################
        ukupna_suma_cena_lokala_decimal = Lokali.objects.values('cena_lokala').aggregate(Sum('cena_lokala'))

        ukupna_suma_cena_lokala = format_decimal(ukupna_suma_cena_lokala_decimal['cena_lokala__sum'], locale='sr_RS')

        # Return API Structure 'ukupan_roi_lokala'
        ukupan_roi_lokala = {
            'ukupan_roi_lokala':
                {
                    'suma_cena_lokala_lamela_l1': ukupna_suma_cena_lamela_l1,
                    'suma_cena_lokala_lamela_l2': ukupna_suma_cena_lamela_l2,
                    'suma_cena_lokala_lamela_l3': ukupna_suma_cena_lamela_l3,
                    'ukupna_suma_cena_lokala': ukupna_suma_cena_lokala,
                }
        }

        return Response(
            kvadratura_lokala | ukupna_suma_lokala_po_lameli | ukupan_roi_lokala
        )

