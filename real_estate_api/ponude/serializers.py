from rest_framework import serializers
from rest_framework.reverse import reverse

from .views import *


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

    adresa_stana = serializers.ReadOnlyField()  # Get field 'Adresa Stana' from 'Ponuda' model
    cena_stana = serializers.ReadOnlyField()  # Get field 'Cena Stana' from 'Ponuda' model

    class Meta:
        model = Ponude
        fields = (
            'id_ponude',
            'kupac',
            'stan',
            'adresa_stana',
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

    def get_detalji_ponude_url(self, obj):
        """Prosledi API putanju do detalja Ponuda"""
        return reverse('ponude:detalji_ponude', args=[obj.pk])

    def get_izmeni_ponudu_url(self, obj):
        """Prosledi Izmeni Ponudu API putnju"""
        return reverse('ponude:izmeni_ponudu', args=[obj.pk])

    def get_obrisi_ponudu_url(self, obj):
        """Prosledjivanje API putanje za brisanje Ponude"""
        return reverse('ponude:obrisi_ponudu', args=[obj.pk])

    def get_kreiraj_ponudu_url(self, obj):
        """Prosledjivanje API putanje za kreiranje Ponude"""
        return reverse('ponude:kreiraj_ponudu')

    def get_lista_ponuda_url(self, obj):
        """Prosledjivanje API putanje do prikaza svih Ponuda"""
        return reverse('ponude:lista_ponuda')


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
