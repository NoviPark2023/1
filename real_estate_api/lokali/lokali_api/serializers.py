from rest_framework import serializers, generics
from rest_framework.reverse import reverse
from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class ListaPonudaLokalaSerializer(serializers.ModelSerializer):
    """
    Listing 'Ponuda' for every 'Lokal'
    """
    detalji_kupca_lokala_url = serializers.SerializerMethodField()
    detalji_ponude_lokala_url = serializers.SerializerMethodField()

    datum_ugovora_lokala = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])
    adresa_lokala = serializers.ReadOnlyField()  # Get field 'Adresa Lokala' from 'PonudaLokala' model
    cena_lokala = serializers.ReadOnlyField()  # Get field 'Cena Lokala' from 'PonudaLokala' model

    class Meta:
        model = PonudeLokala
        fields = (
            "id_ponude_lokala",
            "id_lokala",
            "kupac_lokala",
            "ime_kupca_lokala",
            'adresa_lokala',
            'cena_lokala',
            "cena_lokala_za_kupca",
            "napomena_ponude_lokala",
            "broj_ugovora_lokala",
            "datum_ugovora_lokala",
            "status_ponude_lokala",
            "nacin_placanja_lokala",
            'odobrenje_kupovine_lokala',
            "detalji_kupca_lokala_url",
            "detalji_ponude_lokala_url",
        )

    def get_detalji_kupca_lokala_url(self, obj):
        """Prosledi u API putanju do detalja kupca lokala"""
        return reverse("kupci:detalji_kupca", args=[obj.kupac_lokala.id_kupca])

    def get_detalji_ponude_lokala_url(self, obj):
        """Prosledi u API putanju do detalja ponude lokala"""
        return reverse("ponude-lokali:detalji_ponude_lokala", args=[obj.id_ponude_lokala])


class LokaliSerializer(serializers.ModelSerializer):
    """
    API Listing 'Lokala' Serijalazers.
    """

    detalji_lokala_url = serializers.SerializerMethodField()

    # Inline lista ponuda lokala
    lista_ponuda_lokala = ListaPonudaLokalaSerializer(many=True, read_only=True)
    # Ukupan broj Ponuda za jedan Lokal
    broj_ponuda_za_lokal = serializers.SerializerMethodField()

    class Meta:
        model = Lokali
        fields = (
            "id_lokala",
            "lamela_lokala",
            "adresa_lokala",
            "kvadratura_lokala",
            "broj_prostorija",
            "napomena_lokala",
            "orijentisanost_lokala",
            "status_prodaje_lokala",
            "cena_lokala",
            "lista_ponuda_lokala",
            "broj_ponuda_za_lokal",
            "detalji_lokala_url"
        )

    @staticmethod
    def get_broj_ponuda_za_lokal(obj):
        """
        Ukupan broj ponuda za svaki lokal. Suma ponuda jednog lokala.
        :param obj: ForeignKey in Lokali ka PonudiLokala
        :return: ukupan broj Ponuda za jedan Lokal
        """
        broj_ponuda_lokali = PonudeLokala.objects.select_related('lokal').filter(lokali_id=obj.id_lokala).count()
        return broj_ponuda_lokali

    def get_detalji_lokala_url(self, obj):
        """Prosledi u API putanju do detalji lokala"""
        return reverse("lokali:detalji_lokala", args=[obj.pk])


class BrojPonudaLokalaPoMesecimaSerializer(serializers.ModelSerializer):
    """
    Ukupan broj Ponuda za svaki Lokal po MESECIMA.
    """

    class Meta:
        model = PonudeLokala
        fields = (
            "id_ponude_lokala",
        )


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
