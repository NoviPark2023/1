from decimal import Decimal

from rest_framework import serializers, generics
from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude


class PonudeSerializer(serializers.ModelSerializer):
    """
    Ponude sa redukovanim poljima koje poseduje za prikaz u tabeli i u slucaju responiva u frontendu.
    """
    datum_ugovora = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])
    detalji_ponude_url = serializers.SerializerMethodField()
    izmeni_ponudu_url = serializers.SerializerMethodField()
    obrisi_ponudu_url = serializers.SerializerMethodField()
    kreiraj_ponudu_url = serializers.SerializerMethodField()
    lista_ponuda_url = serializers.SerializerMethodField()

    cena_stana = serializers.SerializerMethodField()  # Get field 'Cena Stana' from 'Ponuda' model

    adresa_stana = serializers.ReadOnlyField()  # Get field 'Adresa Stana' from 'Ponuda' model
    ime_kupca = serializers.ReadOnlyField()  # Get field 'ime_kupca Stana' from 'Ponuda' model
    lamela_stana = serializers.ReadOnlyField()  # Get field 'ime_kupca Stana' from 'Ponuda' model

    class Meta:
        model = Ponude
        fields = (
            'id_ponude',
            'kupac',
            "ime_kupca",
            'stan',
            'adresa_stana',
            'lamela_stana',
            'cena_stana',
            'cena_stana_za_kupca',
            'napomena',
            'broj_ugovora',
            'datum_ugovora',
            'status_ponude',
            'nacin_placanja',
            'odobrenje',
            "klijent_prodaje",
            'detalji_ponude_url',
            'izmeni_ponudu_url',
            'obrisi_ponudu_url',
            'kreiraj_ponudu_url',
            'lista_ponuda_url',
        )

    @staticmethod
    def get_cena_stana(obj):
        """
        Konverzija polja "cena_stana" u float broj i zaokruzivanje decimale na 2 polja.
        @param obj: Ponude
        @return: cena stana (float) rounded 2 decimale.
        """
        cena_stana = float(Decimal(obj.cena_stana))
        return round(cena_stana, 2)

    @staticmethod
    def get_detalji_ponude_url(obj):
        """Prosledi API putanju do detalja Ponuda"""
        return reverse('ponude:detalji_ponude', args=[obj.pk])

    @staticmethod
    def get_izmeni_ponudu_url(obj):
        """Prosledi Izmeni Ponudu API putnju"""
        return reverse('ponude:izmeni_ponudu', args=[obj.pk])

    @staticmethod
    def get_obrisi_ponudu_url(obj):
        """Prosledjivanje API putanje za brisanje Ponude"""
        return reverse('ponude:obrisi_ponudu', args=[obj.pk])

    @staticmethod
    def get_kreiraj_ponudu_url(obj):
        """Prosledjivanje API putanje za kreiranje Ponude"""
        return reverse('ponude:kreiraj_ponudu')

    @staticmethod
    def get_lista_ponuda_url(obj):
        """Prosledjivanje API putanje do prikaza svih Ponuda"""
        return reverse('ponude:lista_ponuda')


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
