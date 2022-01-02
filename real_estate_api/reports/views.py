from babel.numbers import format_decimal, parse_decimal
from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.reports.serializers import (
    ReportsSerializer,
    ProdajaStanovaPoKorisnikuSerializer,
    ProdajaStanovaPoKlijentuSerializer,
    RoiSerializer,
)
from real_estate_api.stanovi.models import Stanovi
from rest_framework.response import Response


class StanoviStatistikaAPIView(generics.ListAPIView):
    """ Kreiranje izvestaja za entitet 'STANOVI' """

    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportsSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Kreiranje izvestaja po kriterijumima:
            * STANOVA PO STATUSU PRODAJE
            * STANOVA PO STATUSU PRODAJE %
            * PRODAJA STANOVA PO MESECIMA
            * BROJ PONUDA PO MESECIMA
        ---
        :param request: None
        :param args: None
        :param kwargs: None
        :return: Resposne 'agregacioni_api' gorespomenutih kriterijumima
        """
        stanovi_global_ukupno = Stanovi.objects.all().count()
        stanovi_ukupan_broj = Stanovi.objects.aggregate(ukupno_stanova=Count('id_stana'))

        # ###########################################
        # REPORTS STANOVA PO STATUSU PRODAJE  REPORT
        # ###########################################
        ukupno_stanovi_rezervisan = Stanovi.objects.filter(
            status_prodaje=Stanovi.StatusProdaje.REZERVISAN
        ).aggregate(
            rezervisano=Count('id_stana')
        )
        ukupno_stanovi_dostupan = Stanovi.objects.filter(
            status_prodaje=Stanovi.StatusProdaje.DOSTUPAN
        ).aggregate(
            dostupan=Count('id_stana')
        )
        ukupno_stanovi_prodat = Stanovi.objects.filter(
            status_prodaje=Stanovi.StatusProdaje.PRODAT
        ).aggregate(
            prodat=Count('id_stana')
        )

        # ###############################################
        # REPORTS STANOVA PO STATUSU PRODAJE U %  REPORT
        # ###############################################
        stanovi_rezervisano_procenti = (ukupno_stanovi_rezervisan.get('rezervisano') / stanovi_global_ukupno) * 100
        stanovi_dostupan_procenti = (ukupno_stanovi_dostupan.get('dostupan') / stanovi_global_ukupno) * 100
        stanovi_prodati_procenti = (ukupno_stanovi_prodat.get('prodat') / stanovi_global_ukupno) * 100

        stanovi_agregirano_procenti = {
            # Zaokruzi procente na 2 decimale
            'procenat_rezervisan': round(stanovi_rezervisano_procenti, 2),
            'procenat_dostupan': round(stanovi_dostupan_procenti, 2),
            'procenat_prodat': round(stanovi_prodati_procenti, 2)
        }

        # ####################################
        # PRODAJA STANOVA PO MESECIMA REPORT
        # ####################################
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

        # #################################
        # BROJ PONUDA PO MESECIMA REPORT
        # #################################
        january = Ponude.objects.filter(datum_ugovora__month=1).count()
        february = Ponude.objects.filter(datum_ugovora__month=2).count()
        march = Ponude.objects.filter(datum_ugovora__month=3).count()
        april = Ponude.objects.filter(datum_ugovora__month=4).count()
        may = Ponude.objects.filter(datum_ugovora__month=5).count()
        june = Ponude.objects.filter(datum_ugovora__month=6).count()
        july = Ponude.objects.filter(datum_ugovora__month=7).count()
        august = Ponude.objects.filter(datum_ugovora__month=8).count()
        september = Ponude.objects.filter(datum_ugovora__month=9).count()
        october = Ponude.objects.filter(datum_ugovora__month=10).count()
        november = Ponude.objects.filter(datum_ugovora__month=11).count()
        december = Ponude.objects.filter(datum_ugovora__month=12).count()

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
        january = Ponude.objects.filter(datum_ugovora__month=1).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0
        february = Ponude.objects.filter(datum_ugovora__month=2).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        march = Ponude.objects.filter(datum_ugovora__month=3).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        april = Ponude.objects.filter(datum_ugovora__month=4).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        may = Ponude.objects.filter(datum_ugovora__month=5).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        june = Ponude.objects.filter(datum_ugovora__month=6).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        july = Ponude.objects.filter(datum_ugovora__month=7).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        august = Ponude.objects.filter(datum_ugovora__month=8).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        september = Ponude.objects.filter(datum_ugovora__month=9).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        october = Ponude.objects.filter(datum_ugovora__month=10).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        november = Ponude.objects.filter(datum_ugovora__month=11).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupna_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupna_suma_prodatih_stanova'] or 0

        december = Ponude.objects.filter(datum_ugovora__month=12).filter(
            status_ponude=Ponude.StatusPonude.KUPLJEN).aggregate(
            ukupno_suma_prodatih_stanova=Sum('cena_stana_za_kupca')
        )['ukupno_suma_prodatih_stanova'] or 0

        ukupna_suma_prodatih_stanova = {'ukupna_suma_prodatih_stanova':
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
            stanovi_ukupan_broj |
            ukupno_stanovi_rezervisan |
            ukupno_stanovi_dostupan |
            ukupno_stanovi_prodat |
            stanovi_agregirano_procenti |
            prodaja_po_mesecima |
            broj_ponuda_po_mesecima |
            ukupna_suma_prodatih_stanova
        )
        return Response(agregacioni_api, content_type="application/json")


class ReportsProdajaStanovaPoKorisnikuAPIView(generics.ListAPIView):
    """ Broj svih rezervisanih Stanova po Korisniku (Agentu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Korisnici.objects.all()
    serializer_class = ProdajaStanovaPoKorisnikuSerializer
    pagination_class = None


class ReportsProdajaStanovaPoKlijentuAPIView(generics.ListAPIView):
    """ Broj svih rezervisanih Stanova po Klijentu (Kupcu) """
    permission_classes = [IsAuthenticated, ]
    queryset = Kupci.objects.all()
    serializer_class = ProdajaStanovaPoKlijentuSerializer
    pagination_class = None


class RoiStanovaAPIView(generics.ListAPIView):
    """ Return on investment za Stanove Report"""

    permission_classes = [IsAuthenticated, ]
    serializer_class = RoiSerializer
    pagination_class = None

    @staticmethod
    def suma_stanova_po_lameli(lamela: str) -> str:
        """
        Stanovi se razvrstavaju po Lamelama, ukupno ih ima 3 i to:
            * L1.1.zz  ||  L2.1.zz  || L3.1.zz
            * L1.2.zz  ||  L2.2.zz  || L3.2.zz
            * L1.3.zz  ||  L2.3.zz  || L3.3.zz
            *          . . .
            * L1.7.zz  ||  L2.7.zz  || L3.7.zz
            * L1.PS.zz  ||  L2.PS.zz  || L3.PS.zz
        Strukutra oznake Lamela je:
            * XX.Y.ZZ Ceo hash Lamele
            * XX: Broj Lamela  ||  Y: Broj Sprata  ||  ZZ: Broj Stana

        ---
        :param lamela: str: 'lamela__startswith' -> naziv lamele *(npr. L1.1).
        :return: str: Formatirana (decimal) suma cene stanova po lameli.
        """
        svi_stanovi_po_lameli = Stanovi.objects.values('cena_stana').filter(
            lamela__startswith=lamela).aggregate(Sum('cena_stana'))

        # Format decimala za 'svi_stanovi_po_lameli_l1_1'
        svi_stanovi_po_lameli = format_decimal(
            svi_stanovi_po_lameli['cena_stana__sum'],
            locale='sr_RS')

        return svi_stanovi_po_lameli

    def get(self, request, *args, **kwargs):
        """
        Agregacija APIja za ROI stanova i to po kriterijumima:
            * Ukupna kvadratura Stanova
            * Ukupna kvadratura Stanova sa korekcijom *(sada 3%)

        :param request: None
        :param args: None
        :param kwargs: None
        :return: agregacioni_api za ROI
        """
        # #####################
        # UKUPNO KVADRATA
        # #####################
        # Suma Kvadrata bez korekcije
        stanovi_ukupno_kvadrata = Stanovi.objects.aggregate(
            stanovi_ukupno_kvadrata=Sum('kvadratura')
        )
        # Format decimal places for 'stanovi_ukupno_kvadrata'
        stanovi_ukupno_kvadrata = format_decimal(
            stanovi_ukupno_kvadrata['stanovi_ukupno_kvadrata'],
            locale='sr_RS')

        # #########################
        # UKUPNO KVADRATA KOREKCIJA
        # #########################
        stanovi_ukupno_korekcija_kvadrata = Stanovi.objects.aggregate(
            stanovi_ukupno_korekcija_kvadrata=Sum('kvadratura_korekcija')
        )
        # Format decimal places for 'stanovi_ukupno_korekcija_kvadrata'
        stanovi_ukupno_korekcija_kvadrata = format_decimal(
            stanovi_ukupno_korekcija_kvadrata['stanovi_ukupno_korekcija_kvadrata'],
            locale='sr_RS')

        # Return API Structure 'kvadratura_stanova'
        kvadratura_stanova = {
            'kvadratura_stanova':
                {
                    'stanovi_ukupno_kvadrata': stanovi_ukupno_kvadrata,
                    'stanovi_ukupno_korekcija_kvadrata': stanovi_ukupno_korekcija_kvadrata,

                }
        }

        # #############################
        # SUMA CENE STANOVA PRVI SPRAT
        # #############################
        # LAMELA: PRVI SPRAT LAMELA 1 (L1.1)
        svi_stanovi_po_lameli_l1_1 = self.suma_stanova_po_lameli('L1.1')

        # LAMELA: PRVI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_1 = self.suma_stanova_po_lameli('L2.1')

        # LAMELA: PRVI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_1 = self.suma_stanova_po_lameli('L3.1')

        # #############################
        # SUMA CENE STANOVA DRUGI SPRAT
        # #############################
        # LAMELA: DRUGI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_2 = self.suma_stanova_po_lameli('L1.2')

        # LAMELA: DRUGI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_2 = self.suma_stanova_po_lameli('L2.2')

        # LAMELA: DRUGI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_2 = self.suma_stanova_po_lameli('L3.2')

        # #############################
        # SUMA CENE STANOVA TRECI SPRAT
        # #############################
        # LAMELA: TRECI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_3 = self.suma_stanova_po_lameli('L1.3')

        # LAMELA: TRECI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_3 = self.suma_stanova_po_lameli('L2.3')

        # LAMELA: TRECI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_3 = self.suma_stanova_po_lameli('L3.3')

        # #############################
        # SUMA CENE STANOVA CETVRTI SPRAT
        # #############################
        # LAMELA: CETVRTI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_4 = self.suma_stanova_po_lameli('L1.4')

        # LAMELA: CETVRTI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_4 = self.suma_stanova_po_lameli('L2.4')

        # LAMELA: CETVRTI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_4 = self.suma_stanova_po_lameli('L3.4')

        # #############################
        # SUMA CENE STANOVA PETI SPRAT
        # #############################
        # LAMELA: PETI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_5 = self.suma_stanova_po_lameli('L1.5')

        # LAMELA: PETI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_5 = self.suma_stanova_po_lameli('L2.5')

        # LAMELA: PETI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_5 = self.suma_stanova_po_lameli('L3.5')

        # #############################
        # SUMA CENE STANOVA SESTI SPRAT
        # #############################
        # LAMELA: SESTI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_6 = self.suma_stanova_po_lameli('L1.6')

        # LAMELA: SESTI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_6 = self.suma_stanova_po_lameli('L2.6')

        # LAMELA: SESTI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_6 = self.suma_stanova_po_lameli('L3.6')

        # #############################
        # SUMA CENE STANOVA SEDMI SPRAT
        # #############################
        # LAMELA: SEDMI SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_7 = self.suma_stanova_po_lameli('L1.7')

        # LAMELA: SEDMI SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_7 = self.suma_stanova_po_lameli('L2.7')

        # LAMELA: SEDMI SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_7 = self.suma_stanova_po_lameli('L3.7')

        # #############################
        # SUMA CENE STANOVA PS SPRAT
        # #############################
        # LAMELA: PS SPRAT LAMELA 1 (L1.2)
        svi_stanovi_po_lameli_l1_ps = self.suma_stanova_po_lameli('L1.PS')

        # LAMELA: PS SPRAT LAMELA 2 (L2.1)
        svi_stanovi_po_lameli_l2_ps = self.suma_stanova_po_lameli('L2.PS')

        # LAMELA: PS SPRAT LAMELA 3 (L3.1)
        svi_stanovi_po_lameli_l3_ps = self.suma_stanova_po_lameli('L3.PS')

        # Return API Structure 'ukupna_suma_stanova_po_lameli'
        ukupna_suma_stanova_po_lameli = {
            'ukupna_cena_stanova_po_lamelama':
                {
                    'svi_stanovi_po_lameli_l1_1': svi_stanovi_po_lameli_l1_1,
                    'svi_stanovi_po_lameli_l2_1': svi_stanovi_po_lameli_l2_1,
                    'svi_stanovi_po_lameli_l3_1': svi_stanovi_po_lameli_l3_1,
                    'svi_stanovi_po_lameli_l1_2': svi_stanovi_po_lameli_l1_2,
                    'svi_stanovi_po_lameli_l2_2': svi_stanovi_po_lameli_l2_2,
                    'svi_stanovi_po_lameli_l3_2': svi_stanovi_po_lameli_l3_2,
                    'svi_stanovi_po_lameli_l1_3': svi_stanovi_po_lameli_l1_3,
                    'svi_stanovi_po_lameli_l2_3': svi_stanovi_po_lameli_l2_3,
                    'svi_stanovi_po_lameli_l3_3': svi_stanovi_po_lameli_l3_3,
                    'svi_stanovi_po_lameli_l1_4': svi_stanovi_po_lameli_l1_4,
                    'svi_stanovi_po_lameli_l2_4': svi_stanovi_po_lameli_l2_4,
                    'svi_stanovi_po_lameli_l3_4': svi_stanovi_po_lameli_l3_4,
                    'svi_stanovi_po_lameli_l1_5': svi_stanovi_po_lameli_l1_5,
                    'svi_stanovi_po_lameli_l2_5': svi_stanovi_po_lameli_l2_5,
                    'svi_stanovi_po_lameli_l3_5': svi_stanovi_po_lameli_l3_5,
                    'svi_stanovi_po_lameli_l1_6': svi_stanovi_po_lameli_l1_6,
                    'svi_stanovi_po_lameli_l2_6': svi_stanovi_po_lameli_l2_6,
                    'svi_stanovi_po_lameli_l3_6': svi_stanovi_po_lameli_l3_6,
                    'svi_stanovi_po_lameli_l1_7': svi_stanovi_po_lameli_l1_7,
                    'svi_stanovi_po_lameli_l2_7': svi_stanovi_po_lameli_l2_7,
                    'svi_stanovi_po_lameli_l3_7': svi_stanovi_po_lameli_l3_7,
                    'svi_stanovi_po_lameli_l1_ps': svi_stanovi_po_lameli_l1_ps,
                    'svi_stanovi_po_lameli_l2_ps': svi_stanovi_po_lameli_l2_ps,
                    'svi_stanovi_po_lameli_l3_ps': svi_stanovi_po_lameli_l3_ps,
                }
        }

        # #####################################
        # UKUPNA SUMA CENE STANOVA PO LAMELAMA
        # #####################################
        # Ukupna suma cene Stanova po Lameli L1
        ukupna_suma_cena_lamela_l1 = self.suma_stanova_po_lameli('L1')

        # Ukupna suma cene Stanova po Lameli L1
        ukupna_suma_cena_lamela_l2 = self.suma_stanova_po_lameli('L2')

        # Ukupna suma cene Stanova po Lameli L1
        ukupna_suma_cena_lamela_l3 = self.suma_stanova_po_lameli('L3')

        # ########################
        # UKUPNA SUMA CENE STANOVA
        # ########################
        ukupna_suma_cena_stanova_decimal = Stanovi.objects.values('cena_stana').aggregate(Sum('cena_stana'))

        ukupna_suma_cena_stanova = format_decimal(ukupna_suma_cena_stanova_decimal['cena_stana__sum'], locale='sr_RS')

        # ############################
        # PROSECNA CENA KVADRATA STANA
        # ############################
        prosecna_cena_kvadrata = parse_decimal(
            ukupna_suma_cena_stanova, locale='sr_RS') / parse_decimal(stanovi_ukupno_korekcija_kvadrata,
                                                                      locale='sr_RS')
        # Return API Structure 'ukupan_roi_stanova'
        ukupan_roi_stanova = {
            'ukupan_roi_stanova':
                {
                    'suma_cena_stanova_lamela_l1': ukupna_suma_cena_lamela_l1,
                    'suma_cena_stanova_lamela_l2': ukupna_suma_cena_lamela_l2,
                    'suma_cena_stanova_lamela_l3': ukupna_suma_cena_lamela_l3,
                    'ukupna_suma_cena_stanova': ukupna_suma_cena_stanova,
                    'prosecna_cena_kvadrata': format_decimal(prosecna_cena_kvadrata, locale='sr_RS'),
                }
        }

        return Response(
            kvadratura_stanova | ukupna_suma_stanova_po_lameli | ukupan_roi_stanova
        )
