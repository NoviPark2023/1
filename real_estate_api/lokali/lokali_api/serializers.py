from rest_framework import serializers, generics

from real_estate_api.lokali.lokali_api.models import Lokali
from rest_framework.reverse import reverse


class LokaliSerializer(serializers.ModelSerializer):
    """
    API Listing 'Lokala' Serijalazers.
    Ukljucene API putanje (API URLs) su:
    ------------------------------------
    * kreiranje lokala
    * detalji lokala
    * uredjivanje lokala
    * brisanje lokala
    """
    kreiraj_lokal_url = serializers.SerializerMethodField()
    detalji_lokala_url = serializers.SerializerMethodField()
    izmeni_lokal_url = serializers.SerializerMethodField()
    obrisi_lokal_url = serializers.SerializerMethodField()

    class Meta:
        model = Lokali
        fields = (
            "id_lokala",
            "lamela_lokala",
            "adresa_lokala",
            "kvadratura_lokala",
            "kvadratura_korekcija",
            "iznos_za_korekciju_kvadrature",
            "broj_prostorija",
            "napomena_lokala",
            "orijentisanost_lokala",
            "status_prodaje_lokala",
            "cena_lokala",
            "cena_kvadrata_lokala",
            "kreiraj_lokal_url",
            "detalji_lokala_url",
            "izmeni_lokal_url",
            "obrisi_lokal_url"
        )

    @staticmethod
    def get_kreiraj_lokal_url(self, obj):
        """Prosledi u API putanju do kreiraj lokal"""
        return reverse("lokali:kreiraj_lokal")

    def get_detalji_lokala_url(self, obj):
        """Prosledi u API putanju do detalji lokala"""
        return reverse("lokali:detalji_lokala", args=[obj.pk])

    def get_izmeni_lokal_url(self, obj):
        """Prosledi u API putanju do uredi lokal"""
        return reverse("lokali:izmeni_lokal", args=[obj.pk])

    def get_obrisi_lokal_url(self, obj):
        """Prosledi u API putanju do obrisi lokal"""
        return reverse("lokali:obrisi_lokal", args=[obj.pk])


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
