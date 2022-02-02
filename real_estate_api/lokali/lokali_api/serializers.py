from rest_framework import serializers, generics

from real_estate_api.lokali.lokali_api.models import Lokali


class LokaliSerializer(serializers.ModelSerializer):
    """
    API Listing 'Lokala' Serijalazers.
    """

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
        )


class FileDownloadListAPI(generics.GenericAPIView):
    """Swagger complain if not register this empty serializers"""
    pass
