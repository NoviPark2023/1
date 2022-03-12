from rest_framework import serializers

from .models import StanoviDms


class StanoviDmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StanoviDms
        fields = (
            "id_fajla",
            "naziv_fajla",
            "datum_ucitavanja",
            "stan",
            "lamela_stana_dokumenti",
        )


class StanoviUploadDmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StanoviDms
        fields = (
            "id_fajla",
            "naziv_fajla",
            "datum_ucitavanja",
            "stan",
            "lamela_stana_dokumenti",
            "file",
        )
