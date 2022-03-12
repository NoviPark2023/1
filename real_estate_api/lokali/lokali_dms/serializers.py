from rest_framework import serializers

from .models import LokaliDms


class LokaliDmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LokaliDms
        fields = (
            "id_fajla",
            "naziv_fajla",
            "datum_ucitavanja",
            "lokal",
            "lamela_lokala_dokumenti",
        )


class LokaliUploadDmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LokaliDms
        fields = (
            "id_fajla",
            "naziv_fajla",
            "datum_ucitavanja",
            "lokal",
            "lamela_lokala_dokumenti",
            "file",
        )
