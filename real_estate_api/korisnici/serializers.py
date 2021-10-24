from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.korisnici.views import Korisnici


class KreirajKorisnikaSerializers(serializers.ModelSerializer):
    """Detalji KORISNIKA sa redukovanim poljima koje poseduje za
          prikaz u tabeli i u slucaju responiva u frontendu.
          Ukljucene API putanje (API URLs) su:
          ------------------------------------
          * detalji korisnika
          * uredjivanje korisnika
          * brisanje korisnika
      """
    detalji_korisnika_url = serializers.SerializerMethodField()
    izmeni_korisnika_url = serializers.SerializerMethodField()
    obrisi_korisnika_url = serializers.SerializerMethodField()
    lista_korisnika_url = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "ime",
            "prezime",
            "email",
            "username",
            "password",
            "role",
            "detalji_korisnika_url",
            "izmeni_korisnika_url",
            "obrisi_korisnika_url",
            "lista_korisnika_url"
        )

    def get_detalji_korisnika_url(self, obj):
        """Prosledi u API putanju do detalji kupca"""
        return reverse("korisnici:detalji_korisnika", args=[obj.pk])

    def get_izmeni_korisnika_url(self, obj):
        """Prosledi u API putanju do uredi kupca"""
        return reverse("korisnici:izmeni_korisnika", args=[obj.pk])

    def get_lista_korisnika_url(self, obj):
        return reverse("korisnici:lista_korisnika")

    def get_obrisi_korisnika_url(self, obj):
        """Prosledi u API putanju do obrisi kupca"""
        return reverse("korisnici:obrisi_korisnika", args=[obj.pk])

class DetaljiKorisnikaSerializers(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Korisnici
        fields = (
            "id",
            "password",
            "last_login",
            "username",
            "ime",
            "prezime",
            "email",
            "role",
            "date_joined",
            "absolute_url"
        )

    def get_absolute_url(self, obj):
        return reverse("detalji_korisnika")
