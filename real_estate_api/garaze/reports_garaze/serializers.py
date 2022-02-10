from rest_framework import serializers
from real_estate_api.garaze.models import Garaze


class ReportsGarazeSerializer(serializers.ModelSerializer):
    ukupno_garaza = serializers.IntegerField()
    rezervisano_garaza = serializers.IntegerField()
    dostupno_garaza = serializers.IntegerField()
    prodato_garaza = serializers.IntegerField()
    procenat_rezervisanih_garaza = serializers.FloatField()
    procenat_dostupnih_garaza = serializers.FloatField()
    procenat_prodatih_garaza = serializers.FloatField()

    class Meta:
        model = Garaze
        fields = (
            "ukupno_garaza",
            "rezervisano_garaza",
            "dostupno_garaza",
            "prodato_garaza",
            "procenat_rezervisanih_garaza",
            "procenat_dostupnih_garaza",
            "procenat_prodatih_garaza",
        )
