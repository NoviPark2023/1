from rest_framework import serializers

from real_estate_api.garaze.models import Garaze

#
# class ListaPonudaGarazaSerializer(serializers.ModelSerializer):
#     """
#     Listing 'Ponuda' for every 'Stan'
#     """
#
#
#     class Meta:
#         model = Garaze
#         fields = (
#             "id_ponude",
#             "stan_id",
#             "kupac",
#             "ime_kupca",
#             'adresa_stana',
#             'cena_stana',
#             "cena_stana_za_kupca",
#             "napomena",
#             "broj_ugovora",
#             "datum_ugovora",
#             "status_ponude",
#             "nacin_placanja",
#             'odobrenje',
#             "detalji_kupca_url",
#             "detalji_ponude_url",
#         )
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
            "lista_ponuda_garaza",
        )
