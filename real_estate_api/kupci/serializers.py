from rest_framework import serializers
from rest_framework.reverse import reverse

from .views import Kupci
from ..ponude.models import Ponude


class KupciSerializer(serializers.ModelSerializer):
    """
    KUPCI sa redukovanim poljima koje poseduje za
    prikaz u tabeli i u slucaju responiva u frontendu.
        Ukljucene API putanje (API URLs) su:
        ------------------------------------
        * detalji kupca
        * izmeni_kupca
        * obrisi kupca
        * kreiranje kupca
        * lista svih kupca
    """

    detalji_kupca_url = serializers.SerializerMethodField()
    izmeni_kupca_url = serializers.SerializerMethodField()
    obrisi_kupca_url = serializers.SerializerMethodField()
    kreiraj_kupca_url = serializers.SerializerMethodField()
    lista_kupaca_url = serializers.SerializerMethodField()

    class Meta:
        model = Kupci
        fields = (
            "id_kupca",
            "lice",
            "ime_prezime",
            "email",
            "broj_telefona",
            "Jmbg_Pib",
            "adresa",
            'detalji_kupca_url',
            'izmeni_kupca_url',
            'obrisi_kupca_url',
            'kreiraj_kupca_url',
            'lista_kupaca_url',
        )

    def get_detalji_kupca_url(self, obj):
        """Prosledi API putanju do detalji kupca"""
        return reverse("kupci:detalji_kupca", args=[obj.pk])

    def get_izmeni_kupca_url(self, obj):
        """Prosledi API putanju do uredi kupca"""
        return reverse("kupci:izmeni_kupca", args=[obj.pk])

    def get_obrisi_kupca_url(self, obj):
        """Prosledi API putanju do obrisi kupca"""
        return reverse("kupci:obrisi_kupca", args=[obj.pk])

    def get_kreiraj_kupca_url(self, obj):
        return reverse("kupci:kreiraj_kupca")

    def get_lista_kupaca_url(self, obj):
        """Prosledi API putanju do liste kupaca"""

        return reverse("kupci:lista_kupaca")


class DetaljiKupcaSerializer(KupciSerializer):
    """
    Detalji KUPCA sa svim poljima koje poseduje.
    Ukljucene API putanje (API URLs) su:
    ------------------------------------
     * izmeni_kupca
     * obrisi kupca
     * lista svih kupca
    """

    class Meta:
        model = Kupci
        fields = (
            "id_kupca",
            "lice",
            "ime_prezime",
            "email",
            "broj_telefona",
            "Jmbg_Pib",
            "adresa",
            'izmeni_kupca_url',
            'obrisi_kupca_url',
            'lista_kupaca_url',
        )


class ListaPonudaKupcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponude
        fields = (
            "id_ponude",
            "cena_stana_za_kupca",
            "napomena",
            "broj_ugovora",
            "datum_ugovora",
            "status_ponude",
            "nacin_placanja",
            "id_kupca",
            "stan_id",
        )
