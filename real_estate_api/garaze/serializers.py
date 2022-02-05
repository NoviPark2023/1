from rest_framework import serializers
from real_estate_api.garaze.models import Garaze


class GarazeSerializer(serializers.ModelSerializer):
    """
    API Listing 'Garaza' Serijalazers.
    """

    ime_kupca = serializers.ReadOnlyField()  # Get field 'ime_kupca Garaza' from 'Ponuda' model

    class Meta:
        model = Garaze
        fields = (
            "id_garaze",
            "jedinstveni_broj_garaze",
            "cena_garaze",
            "datum_ugovora_garaze",
            "broj_ugovora_garaze",
            "napomena_garaze",
            "status_prodaje_garaze",
            "kupac",
            "ime_kupca",
        )
