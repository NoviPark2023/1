from rest_framework import serializers

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.lokali_api.models import Lokali


class ReportsLokaliSerializer(serializers.ModelSerializer):
    ukupno_lokala = serializers.IntegerField()
    rezervisano = serializers.IntegerField()
    dostupno = serializers.IntegerField()
    prodato = serializers.IntegerField()
    procenat_rezervisanih = serializers.DecimalField(max_digits=15, decimal_places=2)
    procenat_dostupnih = serializers.DecimalField(max_digits=15, decimal_places=2)
    procenat_prodatih = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Lokali
        fields = (
            "ukupno_lokala",
            "rezervisano",
            "dostupno",
            "prodato",
            "procenat_rezervisanih",
            "procenat_dostupnih",
            "procenat_prodatih",
        )


class ProdajaLokalaPoKorisnikuSerializer(serializers.ModelSerializer):
    """
    Serijalazer za report ukupno prodatih Lokala po Korisnicima (Agentima)
    """
    prodati_lokali_korisnici = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "ime",
            "prezime",
            "email",
            "role",
            'prodati_lokali_korisnici'
        )

    @staticmethod
    def get_prodati_lokali_korisnici(obj):
        """
        Ukupan broj prodatih lokala filtriran po klijentu prodaje lokala(korisniku-agentu).
            * klijent Prodaje je zapravo agent prodaje, u sistemu nazvan Korisnik.
        Ponude su filtrirane po id klienta prodaje lokala i po statusu PonudeLokala='KUPLJEN'.
        ---
        :param obj: Korisnici *(Agenti nekretnina - Prodavci)
        :return: PonudeLokala (filtrirane po Korisniku)
        """

        prodati_lokali_korisnici = PonudeLokala.objects.select_related('klijent_prodaje_lokala').filter(
            klijent_prodaje_lokala_id=obj.id).filter(status_ponude_lokala="kupljen").count()

        return prodati_lokali_korisnici


class ProdajaLokalaPoKlijentuSerializer(serializers.ModelSerializer):
    """
    Serijalazer za report ukupno prodatih Lokala po Klijentima (Kupcima)
    """
    potencijalni_lokali_klijenti = serializers.SerializerMethodField()
    rezervisani_lokali_klijenti = serializers.SerializerMethodField()
    prodati_lokali_klijenti = serializers.SerializerMethodField()

    class Meta:
        model = Kupci
        fields = (
            "id_kupca",
            "ime_prezime",
            "email",
            'prodati_lokali_klijenti',
            'rezervisani_lokali_klijenti',
            'potencijalni_lokali_klijenti',
        )

    @staticmethod
    def get_prodati_lokali_klijenti(obj):
        ponude_lokala_po_kupcima = PonudeLokala.objects.select_related('kupac_lokala')
        filter_po_id_kupca = ponude_lokala_po_kupcima.filter(kupac_lokala__id_kupca=obj.id_kupca)
        prodati_lokali_klijenti = filter_po_id_kupca.filter(status_ponude_lokala="kupljen").count()

        return prodati_lokali_klijenti

    @staticmethod
    def get_rezervisani_lokali_klijenti(obj):
        rezervisani_lokali_klijenti = PonudeLokala.objects.select_related('kupac_lokala').filter(
            kupac_lokala__id_kupca=obj.id_kupca).filter(
            status_ponude_lokala="rezervisan").count()

        return rezervisani_lokali_klijenti

    @staticmethod
    def get_potencijalni_lokali_klijenti(obj):
        potencijalni_lokali_klijenti = PonudeLokala.objects.select_related('kupac_lokala').filter(
            kupac_lokala__id_kupca=obj.id_kupca).filter(
            status_ponude_lokala="potencijalan").count()

        return potencijalni_lokali_klijenti


class RoiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lokali
        fields = (
            "id_lokala",
            "broj_prostorija",
            "orijentisanost_lokala",
            "kvadratura_lokala",
            "cena_lokala",
        )
