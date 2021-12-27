from rest_framework import serializers

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
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
    """
    Serijalazer za report ukupno prodatih Stanova po Korisnicima (Agentima)
    """
    prodati_stanovi_korisnici = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "ime",
            "prezime",
            "email",
            "role",
            'prodati_stanovi_korisnici'
        )

    @staticmethod
    def get_prodati_stanovi_korisnici(obj):
        prodati_stanovi_korisnici = Ponude.objects.select_related('klijent_prodaje').filter(
            klijent_prodaje_id=obj.id).filter(
            status_ponude="kupljen").count()

        return prodati_stanovi_korisnici


class ProdajaStanovaPoKlijentuSerializer(serializers.ModelSerializer):
    """
        Serijalazer za report ukupno prodatih Stanova po Klijentima (Prodavcima)
        """
    potencijalan_stanovi_klijenti = serializers.SerializerMethodField()
    rezervisani_stanovi_klijenti = serializers.SerializerMethodField()
    prodati_stanovi_klijenti = serializers.SerializerMethodField()

    class Meta:
        model = Kupci
        fields = (
            "id_kupca",
            "ime_prezime",
            "email",
            'prodati_stanovi_klijenti',
            'rezervisani_stanovi_klijenti',
            'potencijalan_stanovi_klijenti',
        )

    @staticmethod
    def get_prodati_stanovi_klijenti(obj):
        ponude_po_kupcima = Ponude.objects.select_related('kupac')
        filter_po_id_kupca = ponude_po_kupcima.filter(kupac__id_kupca=obj.id_kupca)
        prodati_stanovi_klijenti = filter_po_id_kupca.filter(status_ponude="kupljen").count()

        return prodati_stanovi_klijenti

    @staticmethod
    def get_rezervisani_stanovi_klijenti(obj):
        rezervisani_stanovi_klijenti = Ponude.objects.select_related('kupac').filter(kupac__id_kupca=obj.id_kupca).filter(
            status_ponude="rezervisan").count()

        return rezervisani_stanovi_klijenti

    @staticmethod
    def get_potencijalan_stanovi_klijenti(obj):
        potencijalan_stanovi_klijenti = Ponude.objects.select_related('kupac').filter(
            kupac__id_kupca=obj.id_kupca).filter(
            status_ponude="potencijalan").count()

        return potencijalan_stanovi_klijenti
