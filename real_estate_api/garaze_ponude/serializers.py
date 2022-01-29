from rest_framework import serializers

from real_estate_api.garaze_ponude.models import GarazePonude


class PonudeGarazaSerializer(serializers.ModelSerializer):
    """
    Serijalazers Ponude Garaza.
    """

    class Meta:
        model = GarazePonude
        fields = (
            'id_ponude_garaze',
            'kupac_garaze',
            "ime_kupca_garaze",
            'napomena_ponude_garaze',
            'broj_ugovora_garaze',
            'datum_ugovora_garaze',
            'status_ponude_garaze',
            'nacin_placanja_garaze',
            'odobrenje_ponude_garaze',
        )

#
#
# class FileDownloadListAPI(generics.GenericAPIView):
#     """Swagger complain if not register this empty serializers"""
#     pass
