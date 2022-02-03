from rest_framework import serializers, generics
from rest_framework.reverse import reverse

from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class PonudeLokalaSerializer(serializers.ModelSerializer):
    """
    Ponude sa redukovanim poljima koje poseduje za prikaz u tabeli i u slucaju responiva u frontendu.
    """

    class Meta:
        model = PonudeLokala
        fields = (
            'id_ponude_lokala',
            'kupac_lokala',
            "ime_kupca_lokala",
            'lokali',
            'adresa_lokala',
            'lamela_lokala',
            'cena_lokala',
            'napomena_ponude_lokala',
            'broj_ugovora_lokala',
            'datum_ugovora_lokala',
            'status_ponude_lokala',
            'nacin_placanja_lokala',
            'odobrenje_kupovine_lokala',
            'klijent_prodaje_lokala',
        )
