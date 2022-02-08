from rest_framework import serializers

from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class PonudeLokalaSerializer(serializers.ModelSerializer):
    """
    Sva polja iz modela Ponude Lokala i dodatna:
        * cena_lokala : Cena lokala koju je vlasnik odredio.
    """

    cena_lokala = serializers.ReadOnlyField()
    datum_ugovora_lokala = serializers.DateField(format="%d.%m.%Y", input_formats=['%d.%m.%Y', ])

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
            'cena_lokala_za_kupca',
            'napomena_ponude_lokala',
            'broj_ugovora_lokala',
            'datum_ugovora_lokala',
            'status_ponude_lokala',
            'nacin_placanja_lokala',
            'odobrenje_kupovine_lokala',
            'klijent_prodaje_lokala',
        )
