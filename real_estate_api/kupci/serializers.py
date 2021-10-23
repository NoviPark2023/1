from rest_framework import serializers
from rest_framework.reverse import reverse

from real_estate_api.kupci.views import Kupci


class KupciSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

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
            "absolute_url"
        )

    def get_absolute_url(self, obj):
        return reverse("lista_kupaca")


class DetaljiKupcaSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

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
            "update",
        )

    # def get_update(self, obj):
    #     return reverse("uredi_kupca", args=obj.id_kupca, )
    #
    # def get_delete(self, obj):
    #     return reverse("obrisi_kupca", args=obj.id_kupca, )
