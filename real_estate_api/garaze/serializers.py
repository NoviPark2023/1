from rest_framework import serializers
from rest_framework.reverse import reverse
from real_estate_api.garaze.models import Garaze

from real_estate_api.garaze_ponude.serializers import PonudeGarazaSerializer


class GarazeSerializer(serializers.ModelSerializer):
    """
    API Listing 'Garaza' Serijalazers.
    """

    # Inline lista ponuda stana
    lista_ponuda_garaza = PonudeGarazaSerializer(many=True, read_only=True)

    class Meta:
        model = Garaze
        fields = (
            "id_garaze",
            "jedinstveni_broj_garaze",
            "cena_garaze",
            "napomena_garaze",
            "status_prodaje_garaze",
            "lista_ponuda_garaza"
        )
