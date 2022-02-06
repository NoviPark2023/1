from rest_framework import serializers, generics

from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer


class LokaliSerializer(serializers.ModelSerializer):
    """
    API Listing 'Lokala' Serijalazers.
    """

    # Inline lista ponuda stana
    lista_ponuda_lokala = PonudeLokalaSerializer(many=True, read_only=True)

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
        )


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
