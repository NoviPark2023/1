from rest_framework import serializers

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class ReportsSerializer(serializers.ModelSerializer):
    ukupno_stanova = serializers.IntegerField()
    rezervisano = serializers.IntegerField()
    dostupan = serializers.IntegerField()
    prodat = serializers.IntegerField()
    procenat_rezervisan = serializers.DecimalField(max_digits=15, decimal_places=2)
    procenat_dostupan = serializers.DecimalField(max_digits=15, decimal_places=2)
    procenat_prodat = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Stanovi
        fields = (
            "ukupno_stanova",
            "rezervisano",
            "dostupan",
            "prodat",
            "procenat_rezervisan",
            "procenat_dostupan",
            "procenat_prodat",
        )


class ProdajaStanovaPoKorisnikuSerializer(serializers.ModelSerializer):
    prodati_stanovi = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "ime",
            "prezime",
            "email",
            "role",
            'prodati_stanovi'
        )

    @staticmethod
    def get_prodati_stanovi(obj):
        prodati_stanovi_klijenta = Ponude.objects.select_related('klijent_prodaje').filter(
            klijent_prodaje_id=obj.id).filter(
            status_ponude="kupljen").count()

        return prodati_stanovi_klijenta
