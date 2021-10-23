from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.views import exception_handler

from .views import Stanovi
from .models import SlikaStana


class SlikaStanaSerializer(serializers.ModelSerializer):
    """Serijalizers za Slike Stanova"""

    class Meta:
        model = SlikaStana
        fields = ["id_slike", "slika_stana", "alt_text"]


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
    uredi_stan_url = serializers.SerializerMethodField()
    obrisi_stan_url = serializers.SerializerMethodField()

    # Inline slike stana
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
            'detalji_stana_url',
            'uredi_stan_url',
            'obrisi_stan_url',
        )

    def get_detalji_stana_url(self, obj):
        """Prosledi u API putanju do detalji stana"""
        return reverse("detalji_stana", args=[obj.pk])

    def get_uredi_stan_url(self, obj):
        """Prosledi u API putanju do uredi stan"""
        return reverse("uredi_stan", args=[obj.pk])

    def get_obrisi_stan_url(self, obj):
        """Prosledi u API putanju do obrisi stan"""
        return reverse("obrisi_stan", args=[obj.pk])

    def custom_exception_handler(exc, context):
        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)

        # Now add the HTTP status code to the response.
        if response is not None:
            response.data['status_code'] = response.status_code

        return response
