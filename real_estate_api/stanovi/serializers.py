from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude


#from .models import SlikaStana


# class SlikaStanaSerializer(serializers.ModelSerializer):
#     """Serijalizers za Slike Stanova"""
#
#     class Meta:
#         model = SlikaStana
#         fields = ["id_slike", "slika_stana", "alt_text"]


class ListaPonudaStanaSerializer(serializers.ModelSerializer):
    """
    TODO: Komentar za ovaj nested serialilzers
    """
    class Meta:
        model = Ponude
        fields = (
            "kupac",
            "stan_id",
            "id_ponude",
            "cena_stana_za_kupca",
            "napomena",
            "broj_ugovora",
            "datum_ugovora",
            "status_ponude",
            "nacin_placanja",
        )

class StanoviSerializer(serializers.ModelSerializer):
    """
    Detalji STANA sa redukovanim poljima koje poseduje za prikaz u tabeli
    i u slucaju responiva u frontendu.
    Ukljucene API putanje (API URLs) su:
    ------------------------------------
    * detalji stana
    * uredjivanje stana
    * brisanje stana
    """

    detalji_stana_url = serializers.SerializerMethodField()
    izmeni_stan_url = serializers.SerializerMethodField()
    obrisi_stan_url = serializers.SerializerMethodField()
    kreiraj_stan_url = serializers.SerializerMethodField()

    # Inline slike stana
    #slike_stana = SlikaStanaSerializer(many=True, read_only=False)

    # Inline lista ponuda stana
    lista_ponuda_stana= ListaPonudaStanaSerializer(many=True, read_only=True)

    class Meta:
        from .views import Stanovi
        model = Stanovi
        fields = (
            "id_stana",
            "lamela",
            "adresa_stana",
            "kvadratura",
            "sprat",
            "broj_soba",
            "orijentisanost",
            "broj_terasa",
            "cena_stana",
            # "cena_stana_za_kupca",
            "napomena",
            "status_prodaje",
            "klijent_prodaje",
            #"slike_stana",
            #"slike_stana",
            'lista_ponuda_stana',
            'detalji_stana_url',
            'izmeni_stan_url',
            'obrisi_stan_url',
            'kreiraj_stan_url',
        )

    def get_detalji_stana_url(self, obj):
        """Prosledi u API putanju do detalji stana"""
        return reverse("stanovi:detalji_stana", args=[obj.pk])

    def get_izmeni_stan_url(self, obj):
        """Prosledi u API putanju do uredi stan"""
        return reverse("stanovi:izmeni_stan", args=[obj.pk])

    def get_obrisi_stan_url(self, obj):
        """Prosledi u API putanju do obrisi stan"""
        return reverse("stanovi:obrisi_stan", args=[obj.pk])

    def get_kreiraj_stan_url(self, obj):
        return reverse("stanovi:kreiraj_stan")

