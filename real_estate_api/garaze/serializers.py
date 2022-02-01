from rest_framework import serializers
from real_estate_api.garaze.models import Garaze


class GarazeSerializer(serializers.ModelSerializer):
    """
    API Listing 'Garaza' Serijalazers.
    """

    class Meta:
        model = Garaze
        fields = (
            "id_garaze",
            "jedinstveni_broj_garaze",
            "cena_garaze",
            "napomena_garaze",
            "status_prodaje_garaze",
        )
