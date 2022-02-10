from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum

from real_estate_api.garaze.reports_garaze.serializers import ReportsGarazeSerializer
from real_estate_api.garaze.models import Garaze


class GarazeStatistikaAPIView(generics.ListAPIView):
    """ Kreiranje izvestaja za entitet 'GARAZE' """

    permission_classes = [IsAuthenticated, ]
    serializer_class = ReportsGarazeSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Kreiranje izvestaja po kriterijumima:
            * GARAZE PO STATUSU PRODAJE
            * GARAZE PO STATUSU PRODAJE U %
            * PRODAJA GARAZA PO MESECIMA
            * BROJ PONUDA PO MESECIMA
        ---
        :param request: None
        :param args: None
        :param kwargs: None
        :return: Resposne 'agregacioni_api' gorespomenutim kriterijumima
        """
        garaze_global_ukupno = Garaze.objects.all().count()
        garaze_ukupan_broj = Garaze.objects.aggregate(ukupno_garaza=Count('id_garaze'))

        # ########################################
        # REPORTS GARAZE PO STATUSU PRODAJE GARAZA
        # ########################################
        ukupno_garaze_rezervisane = Garaze.objects.filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.REZERVISANA
        ).aggregate(
            rezervisano_garaza=Count('id_garaze')
        )
        ukupno_garaze_dostupne = Garaze.objects.filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.DOSTUPNA
        ).aggregate(
            dostupno_garaza=Count('id_garaze')
        )
        ukupno_garaze_prodate = Garaze.objects.filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA
        ).aggregate(
            prodato_garaza=Count('id_garaze')
        )

        # ############################################
        # REPORTS GARAZE PO STATUSU PRODAJE GARAZA U %
        # ############################################
        try:
            garaze_rezervisane_procenti = (ukupno_garaze_rezervisane.get('rezervisano_garaza') / garaze_global_ukupno) * 100
            garaze_dostupne_procenti = (ukupno_garaze_dostupne.get('dostupno_garaza') / garaze_global_ukupno) * 100
            garaze_prodate_procenti = (ukupno_garaze_prodate.get('prodato_garaza') / garaze_global_ukupno) * 100
        except ZeroDivisionError:
            garaze_rezervisane_procenti = 0
            garaze_dostupne_procenti = 0
            garaze_prodate_procenti = 0

        garaze_agregirano_procenti = {
            # Zaokruzi procente na 2 decimale
            'procenat_rezervisanih_garaza': round(garaze_rezervisane_procenti, 2),
            'procenat_dostupnih_garaza': round(garaze_dostupne_procenti, 2),
            'procenat_prodatih_garaza': round(garaze_prodate_procenti, 2)
        }

        # #################################
        # PRODAJA GARAZA PO MESECIMA REPORT
        # #################################
        january = Garaze.objects.filter(datum_ugovora_garaze__month=1).filter(status_prodaje_garaze='prodata').count()
        february = Garaze.objects.filter(datum_ugovora_garaze__month=2).filter(status_prodaje_garaze='prodata').count()
        march = Garaze.objects.filter(datum_ugovora_garaze__month=3).filter(status_prodaje_garaze='prodata').count()
        april = Garaze.objects.filter(datum_ugovora_garaze__month=4).filter(status_prodaje_garaze='prodata').count()
        may = Garaze.objects.filter(datum_ugovora_garaze__month=5).filter(status_prodaje_garaze='prodata').count()
        june = Garaze.objects.filter(datum_ugovora_garaze__month=6).filter(status_prodaje_garaze='prodata').count()
        july = Garaze.objects.filter(datum_ugovora_garaze__month=7).filter(status_prodaje_garaze='prodata').count()
        august = Garaze.objects.filter(datum_ugovora_garaze__month=8).filter(status_prodaje_garaze='prodata').count()
        september = Garaze.objects.filter(datum_ugovora_garaze__month=9).filter(status_prodaje_garaze='prodata').count()
        october = Garaze.objects.filter(datum_ugovora_garaze__month=10).filter(status_prodaje_garaze='prodata').count()
        november = Garaze.objects.filter(datum_ugovora_garaze__month=11).filter(status_prodaje_garaze='prodata').count()
        december = Garaze.objects.filter(datum_ugovora_garaze__month=12).filter(status_prodaje_garaze='prodata').count()

        prodaja_garaza_po_mesecima = {'prodaja_garaza_po_mesecima':
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

        # ########################################
        # BROJ PONUDA ZA GARAZE PO MESECIMA REPORT
        # ########################################
        january = Garaze.objects.filter(datum_ugovora_garaze__month=1).filter(status_prodaje_garaze='rezervisana').count()
        february = Garaze.objects.filter(datum_ugovora_garaze__month=2).filter(status_prodaje_garaze='rezervisana').count()
        march = Garaze.objects.filter(datum_ugovora_garaze__month=3).filter(status_prodaje_garaze='rezervisana').count()
        april = Garaze.objects.filter(datum_ugovora_garaze__month=4).filter(status_prodaje_garaze='rezervisana').count()
        may = Garaze.objects.filter(datum_ugovora_garaze__month=5).filter(status_prodaje_garaze='rezervisana').count()
        june = Garaze.objects.filter(datum_ugovora_garaze__month=6).filter(status_prodaje_garaze='rezervisana').count()
        july = Garaze.objects.filter(datum_ugovora_garaze__month=7).filter(status_prodaje_garaze='rezervisana').count()
        august = Garaze.objects.filter(datum_ugovora_garaze__month=8).filter(status_prodaje_garaze='rezervisana').count()
        september = Garaze.objects.filter(datum_ugovora_garaze__month=9).filter(status_prodaje_garaze='rezervisana').count()
        october = Garaze.objects.filter(datum_ugovora_garaze__month=10).filter(status_prodaje_garaze='rezervisana').count()
        november = Garaze.objects.filter(datum_ugovora_garaze__month=11).filter(status_prodaje_garaze='rezervisana').count()
        december = Garaze.objects.filter(datum_ugovora_garaze__month=12).filter(status_prodaje_garaze='rezervisana').count()

        broj_ponuda_za_garaze_po_mesecima = {'broj_ponuda_za_garaze_po_mesecima':
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

        # ##########################
        # RAST PRODAJE GARAZA REPORT
        # ##########################
        january = Garaze.objects.filter(datum_ugovora_garaze__month=1).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        february = Garaze.objects.filter(datum_ugovora_garaze__month=2).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        march = Garaze.objects.filter(datum_ugovora_garaze__month=3).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        april = Garaze.objects.filter(datum_ugovora_garaze__month=4).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        may = Garaze.objects.filter(datum_ugovora_garaze__month=5).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        june = Garaze.objects.filter(datum_ugovora_garaze__month=6).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        july = Garaze.objects.filter(datum_ugovora_garaze__month=7).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        august = Garaze.objects.filter(datum_ugovora_garaze__month=8).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        september = Garaze.objects.filter(datum_ugovora_garaze__month=9).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        october = Garaze.objects.filter(datum_ugovora_garaze__month=10).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        november = Garaze.objects.filter(datum_ugovora_garaze__month=11).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        december = Garaze.objects.filter(datum_ugovora_garaze__month=12).filter(
            status_prodaje_garaze=Garaze.StatusProdajeGaraze.PRODATA).aggregate(
            ukupna_suma_prodatih_garaza=Sum('cena_garaze')
        )['ukupna_suma_prodatih_garaza'] or 0

        ukupna_suma_prodatih_garaza = {'ukupna_suma_prodatih_garaza':
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
            garaze_ukupan_broj |
            ukupno_garaze_rezervisane |
            ukupno_garaze_dostupne |
            ukupno_garaze_prodate |
            garaze_agregirano_procenti |
            prodaja_garaza_po_mesecima |
            broj_ponuda_za_garaze_po_mesecima |
            ukupna_suma_prodatih_garaza
        )
        return Response(agregacioni_api, content_type="application/json")
