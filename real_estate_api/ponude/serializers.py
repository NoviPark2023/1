from rest_framework import serializers
from rest_framework.reverse import reverse

from .views import Ponude


class PonudeSerializer(serializers.ModelSerializer):
    """Detalji Ponuda sa redukovanim poljima koje poseduje za
           prikaz u tabeli i u slucaju responiva u frontendu.
           Ukljucene API putanje (API URLs) su:
           ------------------------------------
            * Detalji ponude
            * Izmeni ponudu
            * Brisanje ponude
            * Kreiranje ponude
            * Lista ponuda
       """

    detalji_ponude_url = serializers.SerializerMethodField()
    izmeni_ponudu_url = serializers.SerializerMethodField()
    obrisi_ponudu_url = serializers.SerializerMethodField()
    kreiraj_ponudu_url = serializers.SerializerMethodField()
    lista_ponuda_url = serializers.SerializerMethodField()

    class Meta:
        model = Ponude
        fields = (
            'id_ponude',
            'kupac',
            'stan',
            'cena_stana_za_kupca',
            'napomena',
            'broj_ugovora',
            'datum_ugovora',
            'status_ponude',
            'nacin_placanja',
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


class DetaljiPonudeSerializer(PonudeSerializer):
    """
    Detalji Ponude sa ukljucenim svim poljima.
    Ukljucene API putanje (API URLs) su:
    -------------------------------------
    * Detalji ponude
    * Izmeni ponudu
    * Brisanje ponude
    * Kreiranje ponude
    * Lista ponuda
    """

    class Meta:
        model = Ponude
        fields = (
            'id_ponude',
            'kupac',
            'stan',
            'cena_stana_za_kupca',
            'napomena',
            'broj_ugovora',
            'datum_ugovora',
            'status_ponude',
            'nacin_placanja',
            'detalji_ponude_url',
            'izmeni_ponudu_url',
            'obrisi_ponudu_url',
            'kreiraj_ponudu_url',
            'lista_ponuda_url',
        )
