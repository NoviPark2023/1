from rest_framework import serializers

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
            "napomena_lokala",
            "orijentisanost_lokala",
            "status_prodaje_lokala"
        )
