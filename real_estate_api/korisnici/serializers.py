from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.korisnici.views import Korisnici


class KreirajKorisnikaSerializers(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

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
            "absolute_url"
        )

    def get_absolute_url(self, obj):
        return reverse("lista_korisnika")


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
