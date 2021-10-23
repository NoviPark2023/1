from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.stanovi.views import Stanovi
from .models import SlikaStana


class SlikaStanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlikaStana
        fields = ["slika_stana", "alt_text"]


class StanoviSerializer(serializers.ModelSerializer):
    # absolute_url = serializers.SerializerMethodField()
    slike_stana = SlikaStanaSerializer(many=True, read_only=True)

    class Meta:
        model = Stanovi
        fields = (
            "id_stana",
            "lamela",
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
            "slike_stana",
        )

        # TODO: Videti ovaj get_absolute_url
        # def get_absolute_url(self, obj):
        #     return reverse("lista_stanova")
