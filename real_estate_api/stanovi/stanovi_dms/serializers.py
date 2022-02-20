from rest_framework import serializers
from .models import StanoviDms
from ..serializers import StanoviSerializer


class StanoviDmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StanoviDms
        fields = (
            "id_fajla",
            "opis_dokumenta",
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
            "opis_dokumenta",
            "naziv_fajla",
            "datum_ucitavanja",
            "stan",
            "lamela_stana_dokumenti",
            "file",
        )
