from rest_framework import serializers
from real_estate_api.garaze.models import Garaze


class GarazeSerializer(serializers.ModelSerializer):
    """
    API Listing 'Garaza' Serijalazers.
    """

    ime_kupca = serializers.ReadOnlyField()  # Get field 'ime_kupca Garaza' from 'Ponuda' model
    datum_ugovora_garaze = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

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
            "nacin_placanja_garaze",
            "kupac",
            "ime_kupca",
        )
